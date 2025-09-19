import asyncio
import json
from datetime import datetime
from websocket_protocol_core import WebSocketProtocolCore

class WebSocketManager:
    def __init__(self):
        self.protocol = WebSocketProtocolCore()
        self.running = False

    async def start(self):
        """启动管理程序主流程"""
        # 显示本地IP
        local_ip = self.protocol.get_local_ip()
        print(f"\n本地IP地址: {local_ip}")

        # 获取并验证端口
        port = await self._get_valid_port()
        if not port:
            print("无法获取有效端口，程序退出")
            return

        # 启动服务器
        start_result = await self.protocol.start_server(port)
        if start_result != 0:
            print("服务器启动失败，程序退出")
            return

        self.running = True
        print(f"\n服务器已启动，监听 {local_ip}:{port}")
        print("----------------------------------------")
        print("输入 'send' 发送消息，输入 'exit' 退出程序")
        print("----------------------------------------\n")

        # 启动消息接收协程
        asyncio.create_task(self._message_listener())

        # 启动命令处理循环
        await self._command_handler()

        # 停止服务器
        await self.protocol.stop_server()
        print("程序已退出")

    async def _get_valid_port(self):
        """获取并验证用户输入的端口"""
        while True:
            try:
                port_input = input("请输入要开启的端口号: ")
                port = int(port_input)
                
                valid, msg = self.protocol.validate_port(port)
                if valid:
                    print(f"端口验证成功: {msg}")
                    return port
                else:
                    print(f"端口验证失败: {msg}，请重新输入")
                    
            except ValueError:
                print("无效的端口格式，请输入整数")
            except Exception as e:
                print(f"获取端口时出错: {str(e)}")

    async def _message_listener(self):
        """监听并显示收到的消息"""
        while self.running:
            try:
                message = await self.protocol.get_next_message()
                if message:
                    print("\n" + "="*50)
                    print(f"新消息 [{datetime.fromisoformat(message['时间']).strftime('%Y-%m-%d %H:%M:%S')}]")
                    print(f"来源: {message['对方IP']}:{message['对方端口']}")
                    print(f"类型: {message['处理类型']} / {message['次一级数据类型']}")
                    print("内容:")
                    print(message['数据内容'])
                    print("="*50 + "\n")
                    
            except Exception as e:
                if self.running:
                    print(f"消息监听出错: {str(e)}")
            
            await asyncio.sleep(0.1)  # 短暂休眠，减少CPU占用

    async def _command_handler(self):
        """处理用户命令"""
        while self.running:
            try:
                # 使用run_in_executor在非阻塞模式下获取用户输入
                command = await asyncio.get_event_loop().run_in_executor(
                    None, input, "请输入命令 (send/exit): "
                )
                
                command = command.strip().lower()
                
                if command == 'exit':
                    self.running = False
                    print("正在停止服务器...")
                    
                elif command == 'send':
                    await self._send_message_interactive()
                    
                else:
                    print("未知命令，请输入 'send' 发送消息或 'exit' 退出")
                    
            except Exception as e:
                print(f"命令处理出错: {str(e)}")

    async def _send_message_interactive(self):
        """交互式发送消息"""
        try:
            # 逐个获取消息参数
            target_ip = input("请输入目标IP地址: ").strip()
            if not target_ip:
                print("目标IP不能为空")
                return

            target_port_input = input("请输入目标端口: ").strip()
            try:
                target_port = int(target_port_input)
            except ValueError:
                print("目标端口必须是整数")
                return

            handle_type = input("请输入处理类型: ").strip() or "message"
            sub_type = input("请输入次一级数据类型: ").strip() or "text"
            content = input("请输入消息内容: ").strip()
            if not content:
                print("消息内容不能为空")
                return

            # 发送消息
            print("\n正在发送消息...")
            success, msg = await self.protocol.send_message(
                target_ip,
                target_port,
                handle_type,
                sub_type,
                content
            )

            # 显示发送结果
            if success:
                print(f"✅ 发送成功: {msg}")
            else:
                print(f"❌ 发送失败: {msg}")
                
        except Exception as e:
            print(f"发送消息时出错: {str(e)}")

if __name__ == "__main__":
    try:
        manager = WebSocketManager()
        asyncio.run(manager.start())
    except KeyboardInterrupt:
        print("\n用户中断，程序退出")
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
