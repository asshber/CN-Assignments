from time import sleep
import sys
import os
import threading
import socket
import random
from random import randint

# bash command to req infinte time
# while true; do; wget 127.0.0.1:6000/100MB.bin; done;

BUFFER_SIZE = 4096
MAX_CONNECTIONS = 15

server_list = []
server_conn = []
global file
file = open('log.txt','w')

def loadBalance():

    min_index = server_conn.index(min(server_conn))
    file.write(f"{server_list[min_index]} is chosen, active connections: {server_conn}\n")
    file.flush()
    server_conn[min_index] += 1
    return server_list[min_index]

def sendToServer(conn, serverSock):
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssock.connect((serverSock))
    print('Server-Side Socket: ', ssock.getsockname())
    print('Server Connected: ', serverSock)
    data=conn.recv(BUFFER_SIZE)
    ssock.send(data)
    print('Sending data ', ssock.getsockname(), ' ==> ', serverSock)
    while True:
        data=ssock.recv(BUFFER_SIZE)
        if data:
            conn.send(data)
            data = ""
        else:
            break
    sleep(random.randint(10, 25))
    server_conn[server_list.index(serverSock)] -=1
        
    file.flush()
    conn.close()
    ssock.close()

def startLoadBalancer(port):
    clientSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSideSocket.bind(('127.0.0.1', port))
    print('Client-Side socket: ', clientSideSocket.getsockname())
    clientSideSocket.listen(MAX_CONNECTIONS)
    threading.Thread(target=accept_conn,args=(clientSideSocket,)).start()

def accept_conn(clientSideSocket):
    while True:
        try:
            conn, addr = clientSideSocket.accept()
            thread=threading.Thread(target=sendToServer,args=(conn,loadBalance()))
            thread.start()
        except:
            exit()
def serverThread(port):
    os.system("python server.py " + str(port))

def startApplicationServers(startPort, endPort):
    i = startPort
    while i <= endPort:
        server_list.append(('localhost', i))
        server_conn.append(0)
        thread = threading.Thread(target = serverThread, args = (i,))
        thread.start()
        i = i + 1
    if len(server_list) == len(server_conn):
        print(server_list)
        print(server_conn)


startApplicationServers(int(sys.argv[1]), int(sys.argv[2]))
startLoadBalancer(6000)