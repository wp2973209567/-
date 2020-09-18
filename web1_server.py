"""
web server

完成一个类,提供给别人
让他能够用这个类快速的搭建后端web服务

IO多路复用和http训练
"""
from socket import *
from select import select
import re

# 实现具体功能的类
class WebServer:
    def __init__(self,host,port,html=None):
        self.host = host
        self.port = port
        self.html = html
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    def bind(self):
        self.address = (self.host,self.port)
        self.sock.bind(self.address)

    # 启动服务
    def start(self):
        self.sock.listen(5)
        print("Listen the port %d"%self.port)
        # 首先加入监听套接字
        self.rlist.append(self.sock)
        # 循环监控IO发生
        while True:
            rs,ws,xs = select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sock:
                    # 浏览器链接
                    connfd,addr = self.sock.accept()
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                else:
                    # 处理客户端http请求
                    try:
                        self.handle(r)
                    except:
                        self.rlist.remove(r)
                        r.close()
    # 处理客户端请求
    def handle(self,connfd):
        # 浏览器发过来请求
        request = connfd.recv(1024).decode()
        # print(request)

        # 解析请求 (请求内容)
        pattern = r"[A-Z]+\s+(?P<info>/\S*)"
        result = re.match(pattern,request)
        if result:
            # 提取请求内容
            info = result.group("info")
            print("请求内容:",info)
            self.send_response(connfd,info)
        else:
            # 没有匹配到内容
            self.rlist.remove(connfd)
            connfd.close()
            return

    # 组织发送响应
    def send_response(self,connfd,info):
        # 组织文件路径
        if info == '/':
            filename = self.html + "/index.html"
        else:
            filename = self.html + info

        # 打开失败说明文件不存在
        try:
            file = open(filename,'rb')
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry.....</h1>"
            response = response.encode()
        else:
            data = file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n"%(len(data))
            response += "\r\n"
            response = response.encode() + data
        finally:
            # 发送响应给客户端
            connfd.send(response)


if __name__ == '__main__':
    # 1.使用者怎么利用这个类
    # 2.实现类的功能需要使用者提供什么(传参)
    #      地址     网页
    httpd = WebServer(host='0.0.0.0',port=8001,html='./static')
    httpd.start()