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
    #p_socket.bind(('127.0.0.1',port))
    #p_socket.listen(max_connections)


if __name__== "__main__":
    parser=argparse.ArgumentParser(description='Provide a port for proxy server')
    parser.add_argument('-p',help='Provide a port for proxy server')
    arg=parser.parse_args()

    port=int(arg.p)

    print(port)

    if not os.path.isdir(CACHE_DIR):
        os.makedirs(CACHE_DIR)  #All the cached file will go here