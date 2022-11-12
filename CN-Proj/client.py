import socket

clientIPAddr = '127.0.0.1'
clientPort = 555
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(('127.0.0.1', 6000))
clientSocket.send('info.cern.ch'.encode())