
#此库适用于调用巴法云接口，以连接小米小爱同学操作

import socket

def connect_bemfa(uid, topic): #启动连接
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("bemfa.com", 8344))
    subscribe_cmd = f"cmd=1&uid={uid}&topic={topic}\r\n"
    sock.send(subscribe_cmd.encode("utf-8"))
    return sock

def disconnect_bemfa(sock): #断开连接
    if sock:
        sock.close()

def send_message(sock, uid, topic, message): #发送消息
    publish_cmd = f"cmd=2&uid={uid}&topic={topic}&msg={message}\r\n"
    sock.send(publish_cmd.encode("utf-8"))

def receive_raw(sock): #接收消息
    return sock.recv(1024).decode("utf-8").strip()

def parse_message(raw_msg):
    if raw_msg.startswith("cmd=2"):
        params = {}
        for param in raw_msg.split("&"):
            if "=" in param:
                key, value = param.split("=", 1)
                params[key] = value
        return params.get("msg")
    return None



"""
sock = connect_bemfa(uid="你的账号密匙", topic="你的主题") #启动连接服务器，返回连接参数
send_message(sock,uid="你的账号密匙",topic="你的主题", "0") #需在60s发送任意消息维持在线状态
raw = receive_raw(sock) #接收消息
msg = parse_message(raw) #处理消息
disconnect_bemfa(sock) #断开连接
"""
