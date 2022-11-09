import socket
import  threading
import ssl
import os
import datetime

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)


try:
    log_file = open("Log.txt", 'a')
except:
    log_file = open("Log.txt", 'w')
    log_file.close()

http_website_list = []
block_website = ['slate.com', 'www.google.com']

#Logging everything
def log(msg):
    try:
        with open("Log.txt", 'a') as log_file:
            log_file.write("[{:%Y-%m-%d %H:%M:%S}] ".format(datetime.datetime.now()) + str(msg) + "\n")
    except:
        print("Log File Couldn't Be Opened")


#Forwarding data for HTTPS
def forward_data(client, server):
    try:
        while True:
            data = client.recv(65536)
            if data:
                server.sendall(data)
            else:
                break
    except:
        pass

#Parsing HTTP Header and request
def parse(sock, data, addr):
    try:
        first_line = data.split("\n")[0]
        url = first_line.split(" ")[1]

        http_pos = url.find("://")
        if http_pos == -1:
            temp = url
        else:
            temp = url[(http_pos+3):]

        port_pos = temp.find(":")
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)
        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            port = 80
            webserver = temp[:webserver_pos]
        else:
            port = int(temp[(port_pos+1):][:webserver_pos - port_pos - 1])
            webserver = temp[:port_pos]

        if webserver in block_website:
            return
        Handle_HTTP(webserver, port, sock, data)
        sock.close()
    except Exception as e:
        log("Error Handling Request for Client : " + str(addr) + "Because " + e)
        
def initial_handshake(clientsock, addr):

    #finding host and port of the website
    request = clientsock.recv(40960).decode()
    try:
        i = request.find(' ') + 1
        j = request.find(' ', i)
        host, port = request[i : j].split(':')
        port = int(port)

        if host in block_website:
            return

        #Handling HTTP Connection
        if port == 80:
            Handle_HTTP(host, port, clientsock, request)
            return

        #Creating Secure Server Socket
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            serversock = context.wrap_socket(serversock, server_side=True, do_handshake_on_connect=False)
            #Check if the ssl version is supported by the server
            if serversock:
                raise Exception("")
            #Manually doing handshake for 
            serversock.do_handshake()
        except:
            serversock.close()
            serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #Connect to the server
        serversock.connect((host, port))
        log("Connected to HTTPS Server : " + str(host))

        #initial HTTP CONNECT response
        clientsock.sendall(b'HTTP/1.1 200 Connection Established\r\n\r\n')

        #start the communication between client and server
        threading.Thread(target=forward_data, args=(clientsock, serversock,)).start()
        threading.Thread(target=forward_data, args=(serversock, clientsock,)).start()
    except:
        #Also Handling HTTP Connection
        parse(clientsock, request, addr)

def Handle_HTTP(website, port, conn, data):
    try:
        try:#Self Signed Certificate is used
#Creating Secure Context for the connection

            file = open(os.getcwd()+"/Cache/"+website+".html", "r")
            data = file.read()
            conn.sendall(data.encode())
            conn.close()
            return
        except:
            pass
            
        with open(os.getcwd()+"/Cache/"+website+".html", "w") as f:
        
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((website, port))
            log("Connected to HTTP Server : " + str(website))
            s.send(data.encode())
            while True:
                reply = s.recv(65536)
                f.write(reply.decode())
                if len(reply) > 0:
                    conn.sendall(reply)
                else:
                    break        
            
            s.close()
            conn.close()
    except Exception as e:
        log(str(website)+"Couldn't be open because "+e)


def start_proxy():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('127.0.0.1', 8080))
    sock.listen(10)


    while True:
        conn, addr = sock.accept()
        #log("Client connected with address : "+str(addr))
        threading.Thread(target=initial_handshake, args=(conn, addr)).start()

threading.Thread(target=start_proxy, args=()).start()
log("--------------------------      NEW SESSION     --------------------------------------")
print("Usage:\nEnter Add {Website} to add it to block list\nEnter Del {Website} to delete it from block list\nEnter list to get all the blocked websites")

while True:
    website = input("Command -> ")
    try:
        command, website = website.split(" ")
        if command == "Add":
            block_website.append(website)
            log(website+" added to blocklist")
            print(website+" added to the blocklist")
        elif command == "Del":
            try:
                block_website.remove(website)
                print(website+" deleted from the blocklist")
                log(website+" deleted from the blocklist")
            except:
                print("There is no such Website in Block list")
        else:
            raise Exception("D")
    except:
        if website == "list":
            print("Websites :")
            for i in block_website:
                print(i)
        else:
            print("Enter a valid Command")
    

