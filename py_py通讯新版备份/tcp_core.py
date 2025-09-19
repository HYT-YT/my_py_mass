import socket
import threading
import json
import os
import sqlite3
import time
from typing import Tuple, Union, List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor


class TCPCore:
    def __init__(self):
        # 服务器核心状态
        self.recv_sock: Optional[socket.socket] = None  # 接收服务器socket
        self.send_sock: Optional[socket.socket] = None  # 发送服务器socket
        self.recv_running: bool = False                 # 接收服务器运行状态
        self.send_running: bool = False                 # 发送服务器运行状态
        self.recv_port: Optional[int] = None            # 接收服务器端口
        self.send_port: Optional[int] = None            # 发送服务器端口
        self.send_id: Optional[Union[str, bool]] = None # 发送端ID（False=匿名）
        self.target: Optional[Tuple[str, int]] = None   # 当前TCP长连接目标 (IP, 端口)
        self.long_conn: Optional[socket.socket] = None  # TCP长连接实例
        
        # 存储配置
        self.keep_disk: bool = False  # True=磁盘(SQLite)，False=内存
        self.msgs: List[Dict] = []    # 内存消息存储列表
        self.msg_lock = threading.Lock()  # 内存消息锁
        
        # SQLite数据库配置
        self.db_file: str = "tcp_data.db"  # 数据库名
        self.db_conn: Optional[sqlite3.Connection] = None  # 数据库连接
        
        # 线程池配置
        self.pool = ThreadPoolExecutor(max_workers=10)
        
        # 连接管理
        self.connections: Dict[Tuple[str, int], socket.socket] = {}
        self.conn_lock = threading.Lock()
        
        # 连接超时管理
        self.timeout: int = 86400  # 默认超时1天（秒）


    def set_timeout(self, seconds: int) -> bool:
        """设置长连接超时时间"""
        if isinstance(seconds, int) and seconds > 0:
            self.timeout = seconds
            with self.conn_lock:
                for conn in self.connections.values():
                    try:
                        conn.settimeout(seconds)
                    except Exception:
                        pass  # 仅在库崩溃时才打印，此处忽略
            return True
        return False


    def get_conn_count(self) -> int:
        """获取当前已连接的客户端数量"""
        with self.conn_lock:
            return len(self.connections)


    def get_local_ip(self) -> str:
        """获取本机IP地址"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except Exception as e:
            return f"IP获取失败: {str(e)}"


    def check_port(self, port: Union[str, int], is_target: bool = False) -> bool:
        """校验端口是否可用"""
        try:
            port_int = int(port)
            if not (1 <= port_int <= 65535):
                return False
            
            if is_target:
                return True
            
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port_int))
            return True
        except (ValueError, OSError):
            return False


    def _init_db(self) -> bool:
        """初始化SQLite数据库"""
        try:
            self.db_conn = sqlite3.connect(self.db_file, check_same_thread=False)
            cursor = self.db_conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS msgs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    MA TEXT, MB TEXT, MC TEXT, MD TEXT,
                    ID TEXT, MT TEXT, IP TEXT, DK INTEGER,
                    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.db_conn.commit()
            return True
        except Exception as e:
            print(f"数据库初始化崩溃: {str(e)}")  # 库崩溃级错误
            if self.db_conn:
                self.db_conn.close()
                self.db_conn = None
            return False


    def clean_db(self) -> bool:
        """清理残留数据库文件"""
        try:
            if self.db_conn:
                self.db_conn.close()
                self.db_conn = None
            
            current_dir = os.path.dirname(os.path.abspath(__file__)) if __file__ else os.getcwd()
            for filename in os.listdir(current_dir):
                if filename.startswith("tcp_data") and filename.endswith(".db"):
                    os.remove(os.path.join(current_dir, filename))
            return True
        except Exception as e:
            print(f"数据库清理崩溃: {str(e)}")  # 库崩溃级错误
            return False


    def _store_msg(self, msg: Dict) -> bool:
        """存储接收到的消息"""
        try:
            if not self.keep_disk:
                with self.msg_lock:
                    self.msgs.append(msg)
                return True
            
            if not self.db_conn and not self._init_db():
                return False
            
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO msgs (MA, MB, MC, MD, ID, MT, IP, DK)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                json.dumps(msg.get("MA")),
                json.dumps(msg.get("MB")),
                json.dumps(msg.get("MC")),
                json.dumps(msg.get("MD")),
                json.dumps(msg.get("ID")),
                json.dumps(msg.get("MT")),
                msg.get("IP"),
                msg.get("DK")
            ))
            self.db_conn.commit()
            return True
        except Exception:
            return False


    def _get_mem_msg(self, filter_dict: Optional[Dict] = None) -> Optional[Dict]:
        """从内存获取消息"""
        with self.msg_lock:
            if not self.msgs:
                return None
            
            if not filter_dict:
                return self.msgs.pop(0)
            
            for idx, msg in enumerate(self.msgs):
                msg_id = json.loads(msg["ID"])
                msg_ip = msg["IP"]
                msg_dk = msg["DK"]
                
                match = True
                # 将原"X"判断改为False判断
                if filter_dict.get("sender_id") is not False and str(msg_id) != filter_dict["sender_id"]:
                    match = False
                if filter_dict.get("sender_ip") is not False and msg_ip != filter_dict["sender_ip"]:
                    match = False
                if filter_dict.get("sender_port") is not False and str(msg_dk) != filter_dict["sender_port"]:
                    match = False
                
                if match:
                    return self.msgs.pop(idx)
            return None


    def _get_db_msg(self, filter_dict: Optional[Dict] = None) -> Optional[Dict]:
        """从SQLite获取消息"""
        if not self.db_conn:
            return None
        
        try:
            cursor = self.db_conn.cursor()
            base_sql = "SELECT MA, MB, MC, MD, ID, MT, IP, DK FROM msgs ORDER BY create_time ASC LIMIT 1"
            delete_sql = "DELETE FROM msgs WHERE id = (SELECT id FROM msgs ORDER BY create_time ASC LIMIT 1)"
            
            if filter_dict:
                where_clauses = []
                params = []
                # 将原"X"判断改为False判断
                if filter_dict.get("sender_id") is not False:
                    where_clauses.append("ID = ?")
                    params.append(json.dumps(filter_dict["sender_id"]))
                if filter_dict.get("sender_ip") is not False:
                    where_clauses.append("IP = ?")
                    params.append(filter_dict["sender_ip"])
                if filter_dict.get("sender_port") is not False:
                    where_clauses.append("DK = ?")
                    params.append(int(filter_dict["sender_port"]))
                
                if where_clauses:
                    base_sql = f"SELECT MA, MB, MC, MD, ID, MT, IP, DK FROM msgs WHERE {' AND '.join(where_clauses)} ORDER BY create_time ASC LIMIT 1"
                    delete_sql = f"DELETE FROM msgs WHERE id = (SELECT id FROM msgs WHERE {' AND '.join(where_clauses)} ORDER BY create_time ASC LIMIT 1)"
            
            cursor.execute(base_sql, params if filter_dict else [])
            row = cursor.fetchone()
            if not row:
                return None
            
            cursor.execute(delete_sql, params if filter_dict else [])
            self.db_conn.commit()
            
            return {
                "MA": json.loads(row[0]),
                "MB": json.loads(row[1]),
                "MC": json.loads(row[2]),
                "MD": json.loads(row[3]),
                "ID": json.loads(row[4]),
                "MT": json.loads(row[5]),
                "IP": row[6],
                "DK": row[7]
            }
        except Exception:
            return None


    def start_recv(self, port: Union[str, int], keep_disk: bool) -> bool:
        """启动接收服务器"""
        if keep_disk and not self.clean_db():
            return False
        
        if not self.check_port(port):
            return False
        self.recv_port = int(port)
        self.keep_disk = keep_disk
        
        if keep_disk and not self._init_db():
            return False
        
        try:
            self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.recv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024 * 8)
            self.recv_sock.bind(("", self.recv_port))
            self.recv_sock.listen(5)
            self.recv_running = True
            
            threading.Thread(target=self._recv_loop, daemon=True).start()
            return True
        except Exception as e:
            print(f"接收服务器启动崩溃: {str(e)}")  # 库崩溃级错误
            self.stop_recv()
            return False


    def _recv_loop(self) -> None:
        """接收服务器循环"""
        while self.recv_running:
            try:
                client_sock, client_addr = self.recv_sock.accept()
                client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024 * 8)
                client_sock.settimeout(self.timeout)
                
                self.pool.submit(self._handle_client, client_sock, client_addr)
            except Exception as e:
                if self.recv_running:
                    print(f"接收连接崩溃: {str(e)}")  # 库崩溃级错误


    def _handle_client(self, client_sock: socket.socket, client_addr: Tuple[str, int]) -> None:
        """处理客户端连接"""
        client_ip, client_port = client_addr
        key = (client_ip, client_port)
        
        try:
            with self.conn_lock:
                self.connections[key] = client_sock
            
            while self.recv_running and key in self.connections:
                # 接收消息长度前缀
                length_data = b""
                while len(length_data) < 4:
                    chunk = client_sock.recv(4 - len(length_data))
                    if not chunk:
                        raise ConnectionResetError
                    length_data += chunk
                
                msg_len = int.from_bytes(length_data, byteorder='big')
                
                # 接收消息内容
                data = b""
                remaining = msg_len
                buf_size = 4096 if remaining < 1024 * 1024 else 1024 * 1024
                
                while remaining > 0:
                    chunk = client_sock.recv(min(buf_size, remaining))
                    if not chunk:
                        raise ConnectionResetError
                    data += chunk
                    remaining -= len(chunk)
                
                if not data:
                    continue
                
                msg = json.loads(data.decode("utf-8"), parse_constant=lambda x: x)
                
                # 验证消息字段
                required = {"MA", "MB", "MC", "MD", "ID", "MT"}
                for field in required - msg.keys():
                    msg[field] = False
                
                # 补充网络层信息
                msg["IP"] = client_ip
                msg["DK"] = client_port
                
                self._store_msg(msg)
        
        except json.JSONDecodeError:
            pass
        except (ConnectionResetError, socket.timeout):
            pass
        except Exception as e:
            print(f"消息处理崩溃: {str(e)}")  # 库崩溃级错误
        finally:
            with self.conn_lock:
                if key in self.connections:
                    del self.connections[key]
            
            try:
                client_sock.close()
            except Exception:
                pass


    def start_send(self, send_id: Union[str, bool], port: Union[str, int, bool]) -> bool:
        """启动发送服务器"""
        if self.send_running:
            return False
        
        # 处理发送端ID
        if send_id is False:
            self.send_id = False
        elif send_id == "":
            import random
            self.send_id = "".join([str(random.randint(0, 9)) for _ in range(24)])
        else:
            self.send_id = str(send_id)
        
        # 处理发送端口
        if port is False:
            self.send_port = None
            self.send_running = True
            return True
        elif port == "":
            import random
            for _ in range(10):
                rand_port = random.randint(1024, 65535)
                if self.check_port(rand_port):
                    self.send_port = rand_port
                    break
            if not self.send_port:
                return False
        else:
            if not self.check_port(port):
                return False
            self.send_port = int(port)
        
        # 绑定发送端口
        try:
            self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 8)
            self.send_sock.bind(("", self.send_port))
            self.send_running = True
            
            if self.recv_running and self.send_port:
                threading.Thread(target=self._recv_loop, daemon=True).start()
            return True
        except Exception as e:
            print(f"发送服务器启动崩溃: {str(e)}")  # 库崩溃级错误
            self.stop_send()
            return False


    def send_msg(self, ip: str, port: Union[str, int], 
                MA: Optional[Union[str, None]], MB: Optional[Union[str, None]], 
                MC: Optional[Union[str, None]], MD: Optional[Union[str, None]], 
                ID: Optional[Union[str, None]], MT: Union[bool, str]) -> bool:
        """发送消息"""
        try:
            port_int = int(port)
            # 处理ID参数
            if ID == "":
                if self.send_running and self.send_id is not False:
                    msg_id = self.send_id
                else:
                    import random
                    msg_id = "".join([str(random.randint(0, 9)) for _ in range(24)])
            else:
                msg_id = ID
            
            # 处理MT参数
            msg_mt = str(int(time.time())) if MT is True else MT
            
            # 构建发送消息
            msg = {
                "MA": MA, "MB": MB, "MC": MC, "MD": MD,
                "ID": msg_id, "MT": msg_mt
            }
            
            # 处理TCP长连接
            target = (ip, port_int)
            if self.target != target or not self.long_conn:
                if self.long_conn:
                    try:
                        self.long_conn.close()
                    except Exception:
                        pass
                
                self.long_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.long_conn.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                self.long_conn.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024 * 1024 * 8)
                self.long_conn.settimeout(self.timeout)
                self.long_conn.connect(target)
                self.target = target
            
            # 序列化消息并发送
            msg_str = json.dumps(msg, separators=(',', ':'))
            msg_bytes = msg_str.encode("utf-8")
            self.long_conn.sendall(len(msg_bytes).to_bytes(4, byteorder='big'))
            
            total_sent = 0
            msg_len = len(msg_bytes)
            chunk_size = 4096 if msg_len < 1024 * 1024 else 1024 * 1024
            
            while total_sent < msg_len:
                chunk = msg_bytes[total_sent:total_sent + chunk_size]
                sent = self.long_conn.send(chunk)
                if sent == 0:
                    raise RuntimeError
                total_sent += sent
            
            return True
        except (socket.timeout, ConnectionResetError):
            self.target = None
            if self.long_conn:
                try:
                    self.long_conn.close()
                except Exception:
                    pass
                self.long_conn = None
            return False
        except Exception:
            self.target = None
            if self.long_conn:
                try:
                    self.long_conn.close()
                except Exception:
                    pass
                self.long_conn = None
            return False


    def get_latest(self) -> Tuple[Optional[Dict], bool]:
        """获取最近1条未读消息"""
        try:
            msg = self._get_mem_msg() if not self.keep_disk else self._get_db_msg()
            return (msg, bool(msg))
        except Exception as e:
            print(f"获取消息崩溃: {str(e)}")  # 库崩溃级错误
            return (None, False)


    def get_specified(self, sender_id: Union[str, int, bool], sender_ip: Union[str, bool], sender_port: Union[str, int, bool]) -> Tuple[Optional[Dict], bool]:
        """获取指定发送端的消息"""
        # 处理sender_id参数，如果是False则保持False，否则转换为字符串
        sender_id_val = sender_id if sender_id is False else str(sender_id)
        # 处理sender_ip参数，如果是False则保持False，否则转换为字符串
        sender_ip_val = sender_ip if sender_ip is False else str(sender_ip)
        # 处理sender_port参数，如果是False则保持False，否则转换为字符串
        sender_port_val = sender_port if sender_port is False else str(sender_port)
        
        # 当所有筛选条件都为False时，返回最新消息（不筛选）
        if sender_id is False and sender_ip is False and sender_port is False:
            return self.get_latest()
        
        filter_dict = {
            "sender_id": sender_id_val,
            "sender_ip": sender_ip_val,
            "sender_port": sender_port_val
        }
        
        try:
            msg = self._get_mem_msg(filter_dict) if not self.keep_disk else self._get_db_msg(filter_dict)
            return (msg, bool(msg))
        except Exception as e:
            print(f"获取指定消息崩溃: {str(e)}")  # 库崩溃级错误
            return (None, False)


    def has_unread(self) -> bool:
        """查询是否存在未读消息"""
        try:
            if not self.keep_disk:
                with self.msg_lock:
                    return len(self.msgs) > 0
            else:
                if not self.db_conn:
                    return False
                
                cursor = self.db_conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM msgs")
                return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"查询未读消息崩溃: {str(e)}")  # 库崩溃级错误
            return False


    def has_specified_unread(self, sender_id: Union[str, int, bool], sender_ip: Union[str, bool], sender_port: Union[str, int, bool]) -> bool:
        """查询是否存在指定发送端的未读消息"""
        # 处理sender_id参数，如果是False则保持False，否则转换为字符串
        sender_id_val = sender_id if sender_id is False else str(sender_id)
        # 处理sender_ip参数，如果是False则保持False，否则转换为字符串
        sender_ip_val = sender_ip if sender_ip is False else str(sender_ip)
        # 处理sender_port参数，如果是False则保持False，否则转换为字符串
        sender_port_val = sender_port if sender_port is False else str(sender_port)
        
        # 当所有筛选条件都为False时，查询所有未读消息
        if sender_id is False and sender_ip is False and sender_port is False:
            return self.has_unread()
        
        try:
            if not self.keep_disk:
                with self.msg_lock:
                    for msg in self.msgs:
                        msg_id = json.loads(msg["ID"])
                        msg_ip = msg["IP"]
                        msg_dk = msg["DK"]
                        
                        match = True
                        # 将原"X"判断改为False判断
                        if sender_id is not False and str(msg_id) != sender_id_val:
                            match = False
                        if sender_ip is not False and msg_ip != sender_ip_val:
                            match = False
                        if sender_port is not False and str(msg_dk) != sender_port_val:
                            match = False
                        
                        if match:
                            return True
                return False
            else:
                if not self.db_conn:
                    return False
                
                cursor = self.db_conn.cursor()
                where_clauses = []
                params = []
                
                # 将原"X"判断改为False判断
                if sender_id is not False:
                    where_clauses.append("ID = ?")
                    params.append(json.dumps(sender_id_val))
                if sender_ip is not False:
                    where_clauses.append("IP = ?")
                    params.append(sender_ip_val)
                if sender_port is not False:
                    where_clauses.append("DK = ?")
                    params.append(int(sender_port_val))
                
                query_sql = f"SELECT COUNT(*) FROM msgs WHERE {' AND '.join(where_clauses)}"
                cursor.execute(query_sql, params)
                return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"查询指定未读消息崩溃: {str(e)}")  # 库崩溃级错误
            return False


    def stop_send(self) -> None:
        """停止发送服务器"""
        self.send_running = False
        if self.send_sock:
            try:
                self.send_sock.close()
            except Exception:
                pass
        
        if self.long_conn:
            try:
                self.long_conn.close()
            except Exception:
                pass
        
        self.send_sock = None
        self.send_port = None
        self.send_id = None
        self.target = None
        self.long_conn = None


    def stop_recv(self) -> None:
        """停止接收服务器"""
        self.recv_running = False
        if self.recv_sock:
            try:
                self.recv_sock.close()
            except Exception:
                pass
        
        with self.conn_lock:
            for conn in self.connections.values():
                try:
                    conn.close()
                except Exception:
                    pass
            self.connections.clear()
        
        self.pool.shutdown(wait=False)
        
        if self.keep_disk and self.db_conn:
            try:
                self.db_conn.close()
                if os.path.exists(self.db_file):
                    os.remove(self.db_file)
            except Exception:
                pass
        
        self.recv_sock = None
        self.recv_port = None
        self.db_conn = None
        with self.msg_lock:
            self.msgs = []


    def reset(self) -> None:
        """彻底重置库状态"""
        self.stop_send()
        self.stop_recv()
        self.clean_db()
        self.keep_disk = False


# 简洁接口封装
def check_port(port: Union[str, int], is_target: bool = False) -> bool:
    return _core.check_port(port, is_target)


def start_recv(port: Union[str, int], keep_disk: bool) -> bool:
    return _core.start_recv(port, keep_disk)


def get_latest() -> Tuple[Optional[Dict], bool]:
    return _core.get_latest()


def get_specified(sender_id: Union[str, int, bool], sender_ip: Union[str, bool], sender_port: Union[str, int, bool]) -> Tuple[Optional[Dict], bool]:
    return _core.get_specified(sender_id, sender_ip, sender_port)


def has_unread() -> bool:
    return _core.has_unread()


def has_specified_unread(sender_id: Union[str, int, bool], sender_ip: Union[str, bool], sender_port: Union[str, int, bool]) -> bool:
    return _core.has_specified_unread(sender_id, sender_ip, sender_port)


def start_send(send_id: Union[str, bool], port: Union[str, int, bool]) -> bool:
    return _core.start_send(send_id, port)


def send_msg(ip: str, port: Union[str, int], 
            MA: Optional[Union[str, None]], MB: Optional[Union[str, None]], 
            MC: Optional[Union[str, None]], MD: Optional[Union[str, None]], 
            ID: Optional[Union[str, None]], MT: Union[bool, str]) -> bool:
    return _core.send_msg(ip, port, MA, MB, MC, MD, ID, MT)


def stop_send() -> None:
    _core.stop_send()


def stop_recv() -> None:
    _core.stop_recv()


def reset() -> None:
    _core.reset()


def clean_db() -> bool:
    return _core.clean_db()


def get_conn_count() -> int:
    return _core.get_conn_count()


def set_timeout(seconds: int) -> bool:
    return _core.set_timeout(seconds)


def get_local_ip() -> str:
    return _core.get_local_ip()


# 创建核心实例
_core = TCPCore()



"""

封装函数名：check_port
用途：校验端口是否有效或可用
可传入参数：port (Union[str, int])，is_target (bool，默认False)
传入参数不同值的影响：
  - port：需为1-65535范围内的值，超出此范围返回False
  - is_target为True时仅校验端口格式，为False时还会检查本地是否可绑定该端口
函数会返回那些值及含义：布尔值，True表示端口有效/可用，False表示端口无效/不可用

封装函数名：start_recv
用途：启动本地TCP接收服务，开始监听指定端口并接收消息
可传入参数：port (Union[str, int])，keep_disk (bool)
传入参数不同值的影响：
  - port：需为1-65535范围内的未占用端口，否则启动失败
  - keep_disk为True时消息存储到数据库，为False时存储到内存
函数会返回那些值及含义：布尔值，True表示接收服务启动成功，False表示启动失败

封装函数名：get_latest
用途：获取最新一条未读消息
可传入参数：无
传入参数不同值的影响：无
函数会返回那些值及含义：元组(消息字典, 成功标识)，消息字典为最新消息内容（无消息时为None），成功标识为True表示获取成功

封装函数名：get_specified
用途：获取符合筛选条件的未读消息
可传入参数：sender_id (Union[str, int, bool])，sender_ip (Union[str, bool])，sender_port (Union[str, int, bool])
传入参数不同值的影响：
  - 各参数为False时表示不筛选该条件
  - 三个参数均为False时等价于get_latest()
函数会返回那些值及含义：元组(消息字典, 成功标识)，消息字典为符合条件的消息（无消息时为None），成功标识为True表示获取成功

封装函数名：has_unread
用途：检查是否存在未读消息
可传入参数：无
传入参数不同值的影响：无
函数会返回那些值及含义：布尔值，True表示存在未读消息，False表示无未读消息

封装函数名：has_specified_unread
用途：检查是否存在符合筛选条件的未读消息
可传入参数：sender_id (Union[str, int, bool])，sender_ip (Union[str, bool])，sender_port (Union[str, int, bool])
传入参数不同值的影响：
  - 各参数为False时表示不筛选该条件
  - 三个参数均为False时等价于has_unread()
函数会返回那些值及含义：布尔值，True表示存在符合条件的未读消息，False表示不存在

封装函数名：start_send
用途：启动TCP发送服务，初始化发送端标识和端口
可传入参数：send_id (Union[str, bool])，port (Union[str, int, bool])
传入参数不同值的影响：
  - send_id为False时匿名，为""时自动生成标识，其他值为自定义标识
  - port为False时不绑定端口，为""时自动选择端口，其他值为指定端口
函数会返回那些值及含义：布尔值，True表示发送服务启动成功，False表示启动失败

封装函数名：send_msg
用途：发送TCP消息到指定目标
可传入参数：ip (str)，port (Union[str, int])，MA/MB/MC/MD (Optional)，ID (Optional)，MT (Union[bool, str])
传入参数不同值的影响：
  - ID为""时使用发送端标识或自动生成，其他值为自定义标识
  - MT为True时使用当前时间戳，其他值为自定义时间戳
函数会返回那些值及含义：布尔值，True表示消息发送成功，False表示发送失败

封装函数名：stop_send
用途：停止发送服务并清理相关资源
可传入参数：无
传入参数不同值的影响：无
函数会返回那些值及含义：无返回值

封装函数名：stop_recv
用途：停止接收服务并清理相关资源
可传入参数：无
传入参数不同值的影响：无
函数会返回那些值及含义：无返回值

封装函数名：reset
用途：彻底重置库状态，恢复到初始状态
可传入参数：无
传入参数不同值的影响：无
函数会返回那些值及含义：无返回值

封装函数名：clean_db
用途：清理所有数据库文件并关闭数据库连接
可传入参数：无
传入参数不同值的影响：无
函数会返回那些值及含义：布尔值，True表示清理成功，False表示清理失败

封装函数名：get_conn_count
用途：获取当前已建立的客户端连接数量
可传入参数：无
传入参数不同值的影响：无
函数会返回那些值及含义：整数，当前活跃的客户端连接数

封装函数名：set_timeout
用途：设置TCP长连接的超时时间
可传入参数：seconds (int)
传入参数不同值的影响：仅当seconds为正整数时会更新超时时间并应用到所有连接
函数会返回那些值及含义：布尔值，True表示设置成功，False表示设置失败

封装函数名：get_local_ip
用途：获取本机的IP地址
可传入参数：无
传入参数不同值的影响：无
函数会返回那些值及含义：字符串，本机IP地址；获取失败时返回包含错误信息的字符串

"""








