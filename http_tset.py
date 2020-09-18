"""
http请求　响应示例
"""
from socket import *
sockfd=socket()
sockfd.bind(("0.0.0.0",8888))
sockfd.listen(5)

connfd,addr=sockfd.accept()
print("connect from....",addr)

# 接收到的是来自浏览器的HTTP请求
data=connfd.recv(1024).decode()
print(data.encode())

# 将数据组织为响应
with open("中森明莱.jpg","rb") as f:
    data=f.read()





response="HTTP/1.1 200 OK\r\n"
response+="Content-Type:text/html;charset=utf-8\r\n"
response+="\r\n"
response=response.encode()+data
# 向浏览器发送内容
connfd.send(response)


connfd.close()
sockfd.close()