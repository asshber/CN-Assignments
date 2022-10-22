import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 5555))
sock.listen(1)
conn, addr = sock.accept()
connection = False
while connection == False:
    req = ""
    while req == "":
        req = conn.recv(4096).decode()
    print(req)
    response_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    response_conn.connect(("google.com", 80))
    reply = "HTTP/1.0 200 Connection established\r\n"
    reply += "Proxy-agent: Jarvis\r\n"
    reply += "\r\n"
    conn.sendall(reply.encode())
    # conn.setblocking(0)
    # response_conn.setblocking(0)
    #req = conn.recv(4096)
    response_conn.sendall(req.encode())
    resp = response_conn.recv(4096).decode()
    if(resp != ""):
        connection = True
        print(resp)
        conn.sendall(resp.encode())
        break
   # sock.send("")