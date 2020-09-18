"""
练习 : 将 first.html作为一个要展示的网页
当用户的请求内容是 /first.html的时候则将这个
网页内容作为一个响应体提供给浏览器

如果浏览器请求的是其他内容则 返回一个404的响应,
内容自定

要求浏览器可以循环的访问

思路 : 1 服务端循环模型
      2. 接收到请求后要提取请求内容
      3. 根据请求内容分情况讨论
方案１....
"""
from socket import *
sockfd=socket()
sockfd.bind(("0.0.0.0",8888))
sockfd.listen(5)
while True:
    connfd,addr=sockfd.accept()
    print("connect from....",addr)

    # 接收到的是来自浏览器的HTTP请求
    data=connfd.recv(1024).decode()
    print(data.encode())
    if not data:
        continue
    info=data.split(" ")[1]
    print(info)
    if info=="/first.html":
        # 将数据组织为响应
        response="HTTP/1.1 200 OK\r\n"
        response+="Content-Type:text/html\r\n"
        response+="\r\n"

        with open("first.html") as f:
            msg=f.read().encode()
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
    # 向浏览器发送内容
    connfd.send(response.encode()+msg)
    connfd.close()
sockfd.close()