# from socket import *
#
# serverSocket = socket(AF_INET, SOCK_STREAM)
# # 套接字
# serverSocket.bind(('', 8080))  # 将TCP欢迎套接字绑定到指定端口，可以由任意地址连接
# serverSocket.listen(1)  # 最大连接数为1
#
# while True:
#     print('等待客户端连接')
#     connectionSocket, addr = serverSocket.accept()  # 接收到客户连接请求后，建立新的TCP连接套接字
#     try:
#         message = connectionSocket.recv(1024)    # 获取客户发送的报文
#         filename = message.split()[1]   # 提取报文中的URL，也就是要访问的文件名
#         with open(filename[1:], 'r', encoding='utf-8') as f:
#             outputdata = f.read()
#         # f = open(filename[1:])   # 标记为打开状态
#         # outputdata = f.read()    # 读取文件内容
#         # 返回HTTP响应报文：包含HTTP状态码200和以HTML格式传输的文件内容
#         # 在HTTP协议中，响应报文的第一行和响应头之间必须有一个空白行。这个空白行用于分隔响应头和消息体，因此在发送响应头时需要在最后加上两个换行符\n\n。
#         header = ' HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (
#             len(outputdata))
#         connectionSocket.sendall(header.encode())   # 响应头转换为字节数据发送给客户端
#
#         # 转化为字节数据发送文件内容
#         connectionSocket.sendall(outputdata.encode())
#         connectionSocket.close()
#     except IOError:
#         # 无法响应
#         # header = ' HTTP/1.1 404 Found'
#         # connectionSocket.send(header.encode())
#         # 文件不存在或者打开失败，返回 404 页面
#         with open('404.html', 'r', encoding='utf-8') as f:
#             outputdata = f.read()
#         header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n' % len(outputdata)
#         connectionSocket.sendall(header.encode())
#         connectionSocket.sendall(outputdata.encode())
#
#         # 关闭连接
#         connectionSocket.close()   # 关闭与客户端的TCP请求
# serverSocket.close()   # 关闭服务器监听

import threading
from socket import *


def handle_client(connectionSocket):
    try:
        message = connectionSocket.recv(1024)  # 获取客户发送的报文
        filename = message.split()[1]  #去掉请求的方法，如Get
        # 以utf-8编码格式打开文件
        with open(filename[1:], 'r', encoding='utf-8') as f:
            outputdata = f.read()
        # 发送响应报文头部
        header = ' HTTP/1.1 200 OK\nConnection: close\nContent-Type: text/html\nContent-Length: %d\n\n' % (
            len(outputdata))
        connectionSocket.sendall(header.encode())

        # 发送响应报文消息体
        connectionSocket.sendall(outputdata.encode())
        connectionSocket.close()
    except IOError:
        # # 发送响应报文头部
        # header = ' HTTP/1.1 404 Found'
        # connectionSocket.send(header.encode())
        # 文件不存在或者打开失败，返回 404 页面
        with open('404.html', 'r', encoding='utf-8') as f:
            outputdata = f.read()
        header = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\nContent-Length: %d\r\nConnection: close\r\n\r\n' % len(outputdata)
        connectionSocket.sendall(header.encode())
        connectionSocket.sendall(outputdata.encode())

        connectionSocket.close()


# 创建套接字
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', 8080))  # 将TCP欢迎套接字绑定到指定端口，可以由任意地址连接
serverSocket.listen(5)  # 最大连接数为5

while True:
    print('等待客户端连接')
    connectionSocket, addr = serverSocket.accept()  # 接收到客户连接请求后，建立新的TCP连接套接字
    t = threading.Thread(target=handle_client, args=(connectionSocket,))
    t.start()
