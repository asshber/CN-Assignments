import time
import sys
import os
import threading
import socket
import random

# bash command to req infinte time
# while true; do; curl 127.0.0.1:6000; done;

BUFFER_SIZE = 4096
MAX_CONNECTIONS = 15

threads = []
server_list = []
client_threads=[]


def loadBalance():
    min=999999
    for i in server_list:
        if i[2]<min:
            x=i
            min=i[2]
        else:
            continue
    x[2]+=1
    return x

def sendToServer(conn, serverSock):
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Server-Side Socket: ', ssock.getsockname())
    ssock.connect((serverSock[0], serverSock[1]))
    print('Server Connected: ', serverSock)
    data=conn.recv(BUFFER_SIZE)
    ssock.send(data)
    print('Sending data ', ssock.getsockname(), ' ==> ', serverSock)
    while True:
        data=ssock.recv(BUFFER_SIZE)
        if data:
            conn.send(data)
        else:
            break
    ssock.close()

def startLoadBalancer(port):
    clientSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSideSocket.bind(('127.0.0.1', port))
    print('Client-Side socket: ', clientSideSocket.getsockname())
    clientSideSocket.listen(MAX_CONNECTIONS)
    while True:
        try:
            conn, addr = clientSideSocket.accept()
            thread=threading.Thread(target=sendToServer,args=(conn,loadBalance()))
            client_threads.append(thread)
            thread.start()
        except:
            print(server_list) #To see number of req per server entertained
            exit()


def serverThread(port):
    os.system("python server.py " + str(port))

def startApplicationServers(startPort, endPort):
    i = startPort
    while i <= endPort:
        server_list.append(['localhost', i,0])
        thread = threading.Thread(target = serverThread, args = (i,))
        threads.append(thread)
        thread.start()
        i = i + 1


startApplicationServers(int(sys.argv[1]), int(sys.argv[2]))
startLoadBalancer(6000)