import socket
import argparse
import time
import os
import socket
from _thread import *
import threading
import ssl


max_connections = 5
BUFFER_SIZE = 4096
CACHE_DIR = "./cache"
NO_OF_OCC_FOR_CACHE = 2

def parse(conn):
        req = conn.recv(BUFFER_SIZE)
        #print(req)
        arr=req.split(b'\n')
        #print(arr)
        for i in range(0,len(arr)-2):
            if (i==0):
                method_url=arr[i].split(b' ')
                method=method_url[0]
                url=method_url[1].split(b'://')
                #print(url)
                url_str=url[0]
                if url_str == b'http':
                    url_str=url[1]
                if b':' in url_str:
                    req_port=url_str.split(b':')
                    url_str=req_port[0]
                    req_port=req_port[1]
                else:
                    if(method==b'GET'):
                        # print(url_str)
                        # http_proxy(url_str, 80, conn, req)
                        req_port = 80
                    elif(method == b'CONNECT'):
                        req_port=443
                print(method)
                print(url_str)
                print(req_port)
                if method == b'GET':
                    proxy(url_str, req_port, conn, req)
                elif method ==b'CONNECT':
                    https_proxy(url_str, req_port, conn,req)

def https_proxy(webserver, port, conn, req):
    #print(req)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    filename=webserver
    webserver=webserver.split(b'/')
    webserver=webserver[0]
    os.chdir('/home/asshber/CN-Assignments/A2_Proxy/cache')
    s.connect((webserver, int(port)))
    #Connect ka reply bhejna hy yaha client ko
    s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
    filename=str(filename)
    filename=filename.replace('/','')
    string=bytes(f"GET / HTTP/1.1\r\nHost: {webserver}\r\n\r\n",encoding="utf-8")
    s.sendall(string)
    while True:
        new = s.recv(4096)
        if not new:
            s.close()
            break
        print(new)
        conn.send(new)  

def initialize_proxy():
    p_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    p_socket.bind(('127.0.0.1',port))
    p_socket.listen(max_connections)
    print("Listening...")

    while True:
        #global conn,req
        conn, addr = p_socket.accept()
        #t1=threading.Thread(target=parse,args=(conn))
        print("Connection Request from: " + str(addr[0]) + ", port: " + str(addr[1]))
        start_new_thread(parse, (conn,))
        #t1.start()
        #New fun will be from here threading will also be applied when calling
        # req = conn.recv(BUFFER_SIZE)
        # #print(req)
        # arr=req.split(b'\n')
        # #print(arr)
        # for i in range(0,len(arr)-2):
        #     if (i==0):
        #         method_url=arr[i].split(b' ')
        #         method=method_url[0]
        #         url=method_url[1].split(b'://')
        #         #print(url)
        #         url_str=url[0]
        #         if url_str == b'http':
        #             url_str=url[1]
        #         if b':' in url_str:
        #             req_port=url_str.split(b':')
        #             url_str=req_port[0]
        #             req_port=req_port[1]
        #         else:
        #             if(method==b'GET'):
        #                 # print(url_str)
        #                 # http_proxy(url_str, 80, conn, req)
        #                 req_port = 80
        #             elif(method == b'CONNECT'):
        #                 req_port=443
        #         print(method)
        #         print(url_str)
        #         print(req_port)
        #         proxy(url_str, req_port, conn, req)
            
def proxy(webserver, port, conn, req):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    filename=webserver
    webserver=webserver.split(b'/')
    webserver=webserver[0]
    os.chdir(r'C:\Users\hp\CN-Assignments\A2_Proxy\cache')
    sock.connect((webserver, int(port)))
    filename=str(filename)
    filename=filename.replace('/','')
    #print("Done")
    if filename in os.listdir('.'):
        print("Cache HIT")
        with open(filename,'rb') as f:
            buff=f.read().decode()
        conn.send(buff.encode())
    else:
        print("Cache MISS")
        sock.send(req)
        try:
            buff=sock.recv(BUFFER_SIZE).decode()
        except:
            conn.send("Sorry This proxy cant handle this request".encode())
            exit()
        print(buff)
        with open(filename,'wb') as f:
            f.write(buff.encode())
        conn.send(buff.encode())
            



    

if __name__== "__main__":
    parser=argparse.ArgumentParser(description='Provide a port for proxy server')
    parser.add_argument('-p',help='Provide a port for proxy server')
    arg=parser.parse_args()

    port=int(arg.p)

    print(port)

    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)  #All the cached file will go here

    initialize_proxy()