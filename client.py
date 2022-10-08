from asyncio import windows_events
import socket
import threading
from tkinter import *

def message_send():
   # while True:
        message = Socket_chat.get("0.0", END)
        sock.send(message.encode())
def message_recv(sock):
    while True:
        message = ""
        while message.lower().strip() != 'bye':
            message = sock.recv(1024).decode()
            Socket_output.delete("0.0", END)
            Socket_output.insert(END,message)
            print("Server: ", message)
        #sock.close()


def make_conn():
    data = Socket_data.get()
    data=data.split(':')
    print(data[1])
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((data[0],int(data[1])))
    message = ""

    while message == "":
        message = sock.recv(1024).decode()

    
    print('Received from server: ' + message)
    
    #t1 = threading.Thread(target=message_send, args=(sock,)).start()
    t2 = threading.Thread(target=message_recv, args=(sock,)).start()      

window=Tk()
Socket_lable=Label(window,text="Enter IP Address & Port Number:")
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

Socket_button=Button(window,text="Connect",command=make_conn)
Socket_button.place(x=150,y=30)
window.title('Socket Assignment - Client')
window.geometry("450x400+10+20")
window.mainloop()
