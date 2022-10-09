import socket
import threading
from tkinter import *


def message_send():
    try:
        message = Socket_chat.get("0.0", END)
        Socket_chat.delete("0.0", END)
        conn.send(message.encode())
    except Exception as E:
        Socket_notif.delete("0.0", END)
        Socket_notif.insert(END, "Connect First.")

def message_recv():
    data = ""
    global connection
    while data.lower().strip() != 'bye':
        if connection:
            Socket_notif.delete("0.0", END)    
            Socket_notif.insert(END, "Connected")
        else:
            Socket_notif.delete("0.0", END)
            Socket_notif.insert(END, "Not Connected")
        data = conn.recv(1024).decode()
        Socket_output.delete("0.0", END)
        Socket_output.insert(END,data)
        print(data)    
        #conn.close()

def start_service():
    port = Socket_data.get()
    port=int(port)
    host = "127.0.0.1"
    global sock
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
        Socket_notif.delete("0.0", END)
        Socket_notif.insert(END, "Invalid IP or Port Reenter!")

    print(f"Listening as {host}:{port}")
    global connection
    while connection == False:
        global conn
        conn, addr = sock.accept()
        if addr:
            print("Connected by: ", addr)
            conn.send(("Connection estabilished!").encode())
            connection = True
    t2 = threading.Thread(target=message_recv, args=()).start()

def destroy_window():
    if conn:
        conn.close()
    window.destroy()
    exit()

connection = False
window=Tk()
Socket_lable=Label(window,text="Enter Port Number:")
Socket_lable.place(x=10,y=10)
Socket_data=Entry(window,text="Port",bd=5)
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
Socket_notif=Text(window, height=1.25, width=14, bg="Yellow", font =("Courier", 8), padx=13, pady=10)
Socket_notif.insert(END, "Not Connected")
Socket_notif.place(x=250,y=30)

Socket_button=Button(window,text="Start Listening",command=start_service)
Socket_button.place(x=150,y=30)
window.title('Socket Assignment - Server')
window.geometry("450x400+10+20")
window.mainloop()
window.protocol("WM_DELETE_WINDOW",destroy_window)