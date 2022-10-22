import socket
import argparse
import time
import os
import socket
import threading

max_connections = 5
BUFFER_SIZE = 4096
CACHE_DIR = "./cache"
NO_OF_OCC_FOR_CACHE = 2

def initialize_proxy():
    p_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    p_socket.bind(('127.0.0.1',port))
    p_socket.listen(max_connections)
    print("Listening...")

    while True:
        conn, addr = p_socket.accept()
        print("Connection Request from: " + str(addr[0]) + ", port: " + str(addr[1]))
        #New fun will be from here threading will also be applied when calling
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
                        req_port=80
                    elif(method==b'CONNECT'):
                        req_port=443
                print(method)
                print(url_str)
                print(req_port)
            

    

if __name__== "__main__":
    parser=argparse.ArgumentParser(description='Provide a port for proxy server')
    parser.add_argument('-p',help='Provide a port for proxy server')
    arg=parser.parse_args()

    port=int(arg.p)

    print(port)

    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)  #All the cached file will go here

    initialize_proxy()