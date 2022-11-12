import time
import sys
import os
import threading
import socket
import random

BUFFER_SIZE = 4096
MAX_CONNECTIONS = 15

threads = []
server_list = []


def loadBalance():
    return random.choice(server_list)


def sendToServer(data, serverSock):
    ssock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Server-Side Socket: ', ssock.getsockname())
    ssock.connect((serverSock[0], serverSock[1]))
    print('Server Connected: ', serverSock)
    ssock.send(data)
    print('Sending data ', ssock.getsockname, ' ==> ', serverSock)
    ssock.close()

def startLoadBalancer(port):
    clientSideSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSideSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientSideSocket.bind(('127.0.0.1', port))
    print('Client-Side socket: ', clientSideSocket.getsockname())
    clientSideSocket.listen(MAX_CONNECTIONS)
    conn, addr = clientSideSocket.accept()
    print('Connection from: ', addr)
    data = conn.recv(BUFFER_SIZE)
    print('Received: ', data, ' from: ', addr, ' ==> ', clientSideSocket.getsockname())
    sendToServer(data, loadBalance())

def serverThread(port):
    os.system("python server.py " + str(port))

def startApplicationServers(startPort, endPort):
    i = startPort
    while i <= endPort:
        server_list.append(['localhost', i])
        thread = threading.Thread(target = serverThread, args = (i,))
        threads.append(thread)
        thread.start()
        i = i + 1


startApplicationServers(int(sys.argv[1]), int(sys.argv[2]))
startLoadBalancer(6000)