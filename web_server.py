"""
web server
"""
from socket import *
from select import select
import os,re
#实现其功能的类
class WebServer:
    def __init__(self,host,port,html=None):
        self.host=host
        self.port=port
        self.html=html
        # 提前设置好关注列表
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()
    def create_socket(self):
        self.sockfd=socket()
        self.sockfd.setblocking(False)
    def bind(self):
        self.address=(self.host,self.port)
        self.sockfd.bind(self.address)
    # 启动服务
    def start(self):
        self.sockfd.listen(5)
        self.rlist.append(self.sockfd) # 关注监听套接字
        # 循环监控关注的IO
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            # 遍历就绪的IO列表,分情况讨论 监听套接字和客户端套接字
            for r in rs:
                if r is self.sockfd:
                    #浏览器连接
                    connfd, addr = self.sockfd.accept()
                    print("connect from ....", addr)
                    # 将连接进来的客户端连接套接字加入关注的IO
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    # 处理浏览器请求
                    self.handle(r)
    # 处理浏览器请求
    def handle(self,connfd):
        # 浏览器发送了请求
        data = connfd.recv(1024).decode()
        print(data)
        # 解析请求(请求内容)
        pattern=r"[A-Z]+\s+(?P<info>/\S*"
        result = re.match(pattern, data)
        # if not data:
        #     continue
        # info = data.split(" ")[1]
        if result:
            info=result.group("info")
        print(info)
        if info == self.html:
            # 将数据组织为响应
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"


            with open("first.html") as f:
                msg = f.read().encode()
        else:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
        # 向浏览器发送内容
        connfd.send(response.encode())
        connfd.close()
        self.sockfd.close()


if __name__ == '__main__':
    # 1.使用者怎么利用这个类
    # 2.实现类的功能需要使用者提供什么(传参)
    httpd=WebServer(host="0.0.0.0",port=8800,html="./static")
    httpd.start()