import time
import random
from tcp_core import start_recv, start_send, send_msg, get_latest, has_unread, stop_recv, stop_send, check_port

def main():
    # 配置参数
    target_port = 11  # 默认发送目标端口
    max_port = 65535  # 最大端口号
    min_port = 1024   # 最小端口号（避免使用特权端口）
    max_attempts = 10  # 最大尝试次数
    local_ip = "127.0.0.1"  # 本地IP
    keep_disk = False  # 内存模式
    
    # 首先检查目标端口11是否可用，如果可用就使用它
    found_port = target_port if check_port(target_port) else None
    
    # 如果端口11被占用，随机查找其他可用端口
    if not found_port:
        for _ in range(max_attempts):
            current_port = random.randint(min_port, max_port)
            if check_port(current_port):
                found_port = current_port
                break
    
    if not found_port:
        print(f"无法找到可用端口（尝试了{max_attempts}次）")
        return
    
    # 启动接收服务（内存模式）
    if not start_recv(found_port, keep_disk):
        print(f"启动接收服务失败（端口：{found_port}）")
        return
    
    # 启动发送服务（随机生成ID）
    if not start_send("", False):  # ""表示随机生成ID，False表示不绑定固定发送端口
        print("启动发送服务失败")
        stop_recv()
        return
    
    print(f"服务已启动 - 本地端口: {found_port}")
    print(f"默认发送目标端口: {target_port}")
    print("按Ctrl+C停止服务")
    
    try:
        # 主逻辑：接收用户输入并发送消息
        counter = 1
        while True:
            # 获取用户输入的MA字段（仅需要此字段）
            ma_input = input(f"请输入消息 {counter} 的内容: ")
            
            # 发送消息到目标端口（仅包含MA字段）
            msg_success = send_msg(
                ip=local_ip,
                port=target_port,
                MA=ma_input,  # 仅使用用户输入的MA字段
                MB=None,
                MC=None,
                MD=None,
                ID="",  # 使用默认ID
                MT=True  # 自动生成时间戳
            )
            
            if msg_success:
                print(f"已发送消息 {counter}")
            else:
                print(f"发送消息 {counter} 失败")
            
            # 检查并接收消息
            if has_unread():
                msg, success = get_latest()
                if success and msg:
                    print(f"收到消息: {msg['MA']} (来自: {msg['IP']}:{msg['DK']})")
            
            counter += 1
            print("按Ctrl+C停止服务，或继续输入下一条消息")
            
    except KeyboardInterrupt:
        print("\n正在停止服务...")
    finally:
        # 清理资源
        stop_send()
        stop_recv()
        print("服务已停止")

if __name__ == "__main__":
    main()
