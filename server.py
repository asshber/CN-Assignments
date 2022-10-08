import socket
import threading
from tkinter import *


def message_send():
        message = Socket_chat.get("0.0", END)
        conn.send(message.encode())

def message_recv():
    data = ""
    while data.lower().strip() != 'bye':
        data = conn.recv(1024).decode()
        Socket_output.delete("0.0", END)
        Socket_output.insert(END,data)
        print(data)
    #conn.close()

def start_service():
    port = Socket_data.get()
    port=int(port)
    host = "127.0.0.1"
    sock = socket.socket()
    if (sock != -1):
      print("Socket Created!")
    else:
        print("Socket Creation Failed!")
        exit()
    try:
        sock.bind((host, port))
        sock.listen(1)
    except Exception as E:
        print("Port Error "+ str(E))

    print(f"Listening as {host}:{port}")
    connection = False
    #while True:
    while connection == False:
        global conn
        conn, addr = sock.accept()
        if addr:
            print("Connected by: ", addr)
            conn.send(("Connection estabilished!").encode())
            connection = True
    
    #t1 = threading.Thread(target=message_send, args=(conn,)).start()
    t2 = threading.Thread(target=message_recv, args=()).start()
        
        # msg = input("You: ")
        # conn.send(msg.encode())
        # if msg == "q":
        #     break

        # data = ""
        # while data == "":
        #     data = (conn.recv(2048)).decode()
        # if data == "q":
        #     conn.close()
        #     break
        # else:
        #     print("Server: ", data)
        #     data = ""


window=Tk()
Socket_lable=Label(window,text="Enter  Port Number:")
Socket_lable.place(x=10,y=10)
Socket_data=Entry(window,text="",bd=5)
Socket_data.place(x=10,y=30)
Socket_send_lable=Label(window,text="Type here to send Message:")
Socket_send_lable.place(x=10,y=80)
Socket_chat=Text(window,height=5, width=53)
Socket_chat.place(x=10,y=100)
Socket_send_button=Button(window,text="Send",command=message_send)
Socket_send_button.place(x=400,y=190)
Socket_recv_lable=Label(window,text="Recieved Message:")
Socket_recv_lable.place(x=10,y=220)
Socket_output=Text(window,height=5, width=53)
Socket_output.place(x=10,y=240)

Socket_button=Button(window,text="Connect",command=start_service)
Socket_button.place(x=150,y=30)
window.title('Socket Assignment - Server')
window.geometry("450x400+10+20")
window.mainloop()