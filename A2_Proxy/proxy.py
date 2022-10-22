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

    conn, addr = p_socket.accept()
    print("Connection Request from: " + str(addr[0]) + ", port: " + str(addr[1]))
    req = conn.recv(BUFFER_SIZE)
    print(req)
    arr=req.split(b'\n')
    #print(arr)
    for i in range(0,len(arr)-2):
        if (i==0):
            method_url=arr[i].split(b' ')
            print(method_url)
            method=method_url[0]
            index = method_url[1].find(b"://")
            if(index != -1):
                url = method_url[(index+3)]
            else:
                url = method_url[1]
            print(url)
            port_url = url.split(b':')[1]
            print(port_url)
            file_index = url.find(b'/')
            if(file_index == -1):
                file_index = len(url)

            # url=url_req[1]
            # host_part=url.split(b'/')
            # file_part=host_part[1]
            # host_part=host_part[0]
            print(method)
            # print(host_part)
            # print(file_part)

    

if __name__== "__main__":
    parser=argparse.ArgumentParser(description='Provide a port for proxy server')
    parser.add_argument('-p',help='Provide a port for proxy server')
    arg=parser.parse_args()

    port=int(arg.p)

    print(port)

    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)  #All the cached file will go here

    initialize_proxy()