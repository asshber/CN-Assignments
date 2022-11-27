import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = (('localhost', 6000))
sock.connect(server)
sock.send(b"")