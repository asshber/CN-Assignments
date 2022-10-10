import os
import socket
import threading
import signal
import time
from tkinter import *

def message_send():
        message = Socket_chat.get("0.0", END)
        Socket_chat.delete("0.0", END)
        try:
            sock.send(message.encode())
        except:
            Socket_notif.delete("0.0", END)
            Socket_notif.insert(END, "Connect First")
def message_recv(sock):
        message = ""
        while message.lower().strip() != 'bye':
            global connection
            if connection:
                Socket_notif.delete("0.0", END)    
                Socket_notif.insert(END, "Connected")
            else:
                Socket_notif.delete("0.0", END)
                Socket_notif.insert(END, "Not Connected")
            try:
                message = sock.recv(1024).decode()
            except:
                Socket_notif.delete("0.0", END)
                Socket_notif.insert(END, "Connection Lost")
                time.sleep(10)
                exit()
            Socket_output.delete("0.0", END)
            Socket_output.insert(END,message)
            print("Server: ", message)


def make_conn():
    data = Socket_data.get()
    data=data.split(':')
    global sock
    global connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((data[0],int(data[1])))
    except Exception as E:
        Socket_notif.delete("0.0", END)
        Socket_notif.insert(END, "Invalid IP or Port Reenter!")
    connection = True
    message = ""
    while message == "":
        message = sock.recv(1024).decode()
    print('Received from server: ' + message)
    
    t2 = threading.Thread(target=message_recv, args=(sock,)).start()      


def destroy_window():
    if (connection):
        sock.close()
    window.destroy()
    os.kill(os.getpid(), signal.SIGINT)

global window
window=Tk()
Socket_lable=Label(window,text="Enter IP Address & Port Number:")
Socket_lable.place(x=10,y=10)
connection=False
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
Socket_output=Text(window,height=5, width=53, bg="gray")
Socket_output.place(x=10,y=240)
Socket_notif=Text(window, height=1.25, width=30, bg="Yellow", font =("Courier", 8), padx=2, pady=10)
Socket_notif.insert(END, "Not Connected")
Socket_notif.place(x=220,y=30)

Socket_button=Button(window,text="Connect",command=make_conn)
Socket_button.place(x=150,y=30)
window.title('Socket Assignment - Client')
window.geometry("450x400+10+20")
window.protocol("WM_DELETE_WINDOW", destroy_window ) 
window.mainloop()