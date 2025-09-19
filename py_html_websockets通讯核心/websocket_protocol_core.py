import asyncio
import websockets
import json
import time
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 存储方式配置：1=内存存储，0=磁盘存储
STORAGE_MODE = 1  # 默认内存存储

class WebSocketProtocolCore:
    def __init__(self):
        self.server = None
        self.port = None
        self.is_running = False
        self.received_messages: List[Dict] = []  # 内存存储的消息列表
        self.active_connections = set()  # 活跃的WebSocket连接
        self.data_dir = "data"
        self.message_file = os.path.join(self.data_dir, "received_messages.json")
        
        # 确保数据目录存在
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # 如果使用磁盘存储且文件不存在，初始化文件
        if STORAGE_MODE == 0 and not os.path.exists(self.message_file):
            with open(self.message_file, 'w') as f:
                json.dump([], f)

    def get_local_ip(self) -> str:
        """获取本机IP地址"""
        try:
            # 创建一个临时socket连接来获取本机IP
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            return local_ip
        except Exception as e:
            return f"获取IP失败: {str(e)}"
        
    def validate_port(self, port: int, is_target: bool = False) -> Tuple[bool, str]:
        """校验端口是否有效
        is_target: 是否为目标端口（仅验证格式，不验证是否可用）
        """
        try:
            port = int(port)
            if not (1 <= port <= 65535):
                return False, "端口必须在1-65535之间"
                
            # 如果是目标端口，只验证范围即可，不验证是否被占用
            if is_target:
                return True, f"端口有效: {port}"
                
            # 对于本地端口，需要验证是否可用
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("", port))
            return True, f"端口可用: {port}"
        except ValueError:
            return False, "端口必须是整数"
        except OSError:
            return False, "端口已被占用或无法使用"
    
    async def start_server(self, port: int) -> int:
        """启动WebSocket服务器"""
        try:
            self.port = port
            self.is_running = True
            
            # 创建服务器
            self.server = await websockets.serve(
                self._handle_client, 
                "0.0.0.0",  # 允许所有网络接口访问
                port,
                ping_interval=30,
                ping_timeout=60
            )
            
            print(f"WebSocket服务器已启动，监听端口: {port}")
            return 0  # 启动成功
        except Exception as e:
            print(f"启动服务器失败: {str(e)}")
            return 1  # 启动失败

    async def _handle_client(self, websocket: websockets.WebSocketServerProtocol):
        """处理客户端连接"""
        # 将新连接添加到活跃连接集合
        self.active_connections.add(websocket)
        client_address = websocket.remote_address
        print(f"新连接: {client_address}")
        
        try:
            async for message in websocket:
                await self._process_message(message, client_address)
                
                # 发送确认响应
                response = {
                    "对方IP": client_address[0],
                    "对方端口": client_address[1],
                    "处理类型": "确认",
                    "次一级数据类型": "接收成功",
                    "数据内容": f"已收到消息",
                    "时间": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(response))
                
        except websockets.exceptions.ConnectionClosed:
            print(f"连接关闭: {client_address}")
        except Exception as e:
            print(f"处理客户端消息出错: {str(e)}")
        finally:
            # 从活跃连接集合中移除
            self.active_connections.remove(websocket)

    async def _process_message(self, message: str, client_address: Tuple[str, int]):
        """处理接收到的消息"""
        try:
            message_data = json.loads(message)
            
            # 确保消息包含所有必要字段
            required_fields = ["处理类型", "次一级数据类型", "数据内容", "时间"]
            for field in required_fields:
                if field not in message_data:
                    raise ValueError(f"消息缺少必要字段: {field}")
            
            # 添加发送方信息
            message_data["对方IP"] = client_address[0]
            message_data["对方端口"] = client_address[1]
            
            # 存储消息
            await self._store_message(message_data)
            print(f"收到消息 from {client_address}: {message_data['数据内容'][:30]}...")
            
        except json.JSONDecodeError:
            print(f"无效的JSON消息: {message}")
        except Exception as e:
            print(f"处理消息出错: {str(e)}")

    async def _store_message(self, message: Dict):
        """存储接收到的消息"""
        if STORAGE_MODE == 1:
            # 内存存储
            self.received_messages.append(message)
        else:
            # 磁盘存储
            try:
                with open(self.message_file, 'r') as f:
                    messages = json.load(f)
                messages.append(message)
                with open(self.message_file, 'w') as f:
                    json.dump(messages, f)
            except Exception as e:
                print(f"存储消息到磁盘失败: {str(e)}")

    async def get_next_message(self) -> Optional[Dict]:
        """获取下一条消息并从存储中删除"""
        if STORAGE_MODE == 1:
            # 从内存获取
            if self.received_messages:
                return self.received_messages.pop(0)
            return None
        else:
            # 从磁盘获取
            try:
                with open(self.message_file, 'r') as f:
                    messages = json.load(f)
                if messages:
                    message = messages.pop(0)
                    with open(self.message_file, 'w') as f:
                        json.dump(messages, f)
                    return message
                return None
            except Exception as e:
                print(f"从磁盘读取消息失败: {str(e)}")
                return None

    async def send_message(self, target_ip: str, target_port: int, handle_type: str, sub_type: str, content: str) -> Tuple[bool, str]:
        """发送消息到目标服务器"""
        try:
            uri = f"ws://{target_ip}:{target_port}"
            async with websockets.connect(uri) as websocket:
                message = {
                    "目标IP": target_ip,
                    "目标端口": target_port,
                    "处理类型": handle_type,
                    "次一级数据类型": sub_type,
                    "数据内容": content,
                    "时间": datetime.now().isoformat()
                }
                await websocket.send(json.dumps(message))
                
                # 等待确认响应
                response_data = await websocket.recv()
                if response_data:
                    response = json.loads(response_data)
                    if response.get("处理类型") == "确认":
                        return True, "消息发送成功并收到确认"
                return True, "消息发送成功，但未收到确认"
        except Exception as e:
            return False, f"消息发送失败: {str(e)}"

    async def stop_server(self) -> int:
        """停止服务器"""
        self.is_running = False
        if self.server:
            try:
                self.server.close()
                await self.server.wait_closed()
            except Exception as e:
                print(f"关闭服务器出错: {str(e)}")
        
        # 清理存储
        if STORAGE_MODE == 1:
            self.received_messages = []
        else:
            try:
                with open(self.message_file, 'w') as f:
                    json.dump([], f)
            except Exception as e:
                print(f"清理磁盘存储失败: {str(e)}")
        
        self.port = None
        print("WebSocket服务器已停止")
        return 0  # 停止成功

    async def broadcast(self, handle_type: str, sub_type: str, content: str) -> Tuple[bool, str]:
        """向所有活跃连接广播消息"""
        if not self.active_connections:
            return False, "没有活跃的连接"
            
        message = {
            "目标IP": "broadcast",
            "目标端口": "all",
            "处理类型": handle_type,
            "次一级数据类型": sub_type,
            "数据内容": content,
            "时间": datetime.now().isoformat()
        }
        
        message_str = json.dumps(message)
        tasks = [conn.send(message_str) for conn in self.active_connections]
        
        try:
            await asyncio.gather(*tasks)
            return True, f"已向{len(self.active_connections)}个连接广播消息"
        except Exception as e:
            return False, f"广播消息失败: {str(e)}"
    
