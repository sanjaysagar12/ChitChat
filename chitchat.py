import time
import socket
import random
import threading
from tkinter import *
import tkinter.messagebox as messagebox
from cryptography.fernet import Fernet


class Encryption:
    def Encrypt(self, Key, msg):
        Fernet_Key = Fernet(Key)
        EncryptedMsg = Fernet_Key.encrypt(msg.encode())
        return EncryptedMsg

    def Decrypt(self, Key, msg):
        try:
            Fernet_Key = Fernet(Key)
            DecryptedMsg = Fernet_Key.decrypt(msg).decode()
            return DecryptedMsg
        except:
            return "< Unknown Message >"

    def JumbleKey(self, Key):
        Char_list = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
        Char = ""
        for x in range(2):  # To Junble the Orginal Key for Security Purpose
            for i in range(3):
                Char = Char_list[random.randint(0, 61)] + Char
        Key_Part1 = Key[:23]
        Key_Part2 = Key[23:]

        Key_Part1 = Char[:3].encode() + Key_Part1
        Key_Part2 = Char[3:].encode() + Key_Part2
        Jumbled_Key = Key_Part1 + Key_Part2
        return Jumbled_Key

    def ReassembleKey(self, Jumbled_Key):
        Key_Part1 = Jumbled_Key[3:26]
        Key_Part2 = Jumbled_Key[29:]
        Reassembled_Key = Key_Part1 + Key_Part2
        return Reassembled_Key

class SocketNetworking:
    def Host(self, info):
        global connection, address, Orginal_Key, Encryption
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((info[0], info[1]))
        server.listen(0)
        connection, address = server.accept()

        Orginal_Key = Fernet.generate_key()
        Encryption = Encryption()
        Jumbled_Key = Encryption.JumbleKey(Orginal_Key)
        connection.send(Jumbled_Key)

        Password_Entered = connection.recv(1024)
        Password_Entered = Encryption.Decrypt(Orginal_Key, Password_Entered)

        if Password_Entered == info[3]:
            connection.send("OK".encode())
            return "Verified"
        else:
            connection.send("Wrong Password".encode())
            return "Wrong Password"

    def Connect(self, info):
        global connection, Orginal_Key, Encryption
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((info[0], info[1]))

        Jumbled_Key = connection.recv(1024)
        Encryption = Encryption()
        Orginal_Key = Encryption.ReassembleKey(Jumbled_Key)

        connection.send(Encryption.Encrypt(Orginal_Key, info[3]))
        Verification = connection.recv(1024).decode()

        if Verification == "OK":
            return "Verified"
        else:
            return "Wrong Password"

class DecisionAndUserinfo:
    def HostORConnect(self, ToDo):
        global Do
        if ToDo.get() == 1:
            Do = "Connect"
        else:
            Do = "Host"

    def Submit(self, IP, PORT, user_name, Password):
        global info, SocketNetworking
        SocketNetworking = SocketNetworking()

        if IP != "" and PORT != "" and user_name != "" and Password != "":
            info = [IP, int(PORT), user_name, Password]
            if Do == "Connect":
                Verification = SocketNetworking.Connect(info)

                if Verification == "Verified":
                    GUI.SecondWindow(info)
                else:
                    messagebox.showerror("ERROR", "PASSWORD IS WRONG")
                    GUI1.destroy()
                    exit()
            else:
                Verification = SocketNetworking.Host(info)
                if Verification == "Verified":
                    GUI.SecondWindow(info)
                else:
                    messagebox.showwarning("SECURITY WARNING", "ANONYMOUS PERSON IS TRYING TO LOGIN")
                    GUI1.destroy()
                    exit()

class MainGUI:
    def FirstWindow(self):
        global GUI1
        GUI1 = Tk()
        GUI1.title("Chit Chat")
        GUI1.geometry("350x250")
        GUI1.resizable(width=False, height=False)

        ToDo = IntVar()

        Decision = DecisionAndUserinfo()
        Connect = Radiobutton(GUI1, text="Connect", variable=ToDo, value=1, command=lambda: Decision.HostORConnect(ToDo))
        Host = Radiobutton(GUI1, text="Host", variable=ToDo, value=2, command=lambda: Decision.HostORConnect(ToDo))
        Connect.grid(row=0, column=0)
        Host.grid(row=0, column=1)

        l1 = Label(GUI1, text="Host IP").place(x=20, y=30)
        l2 = Label(GUI1, text="PORT").place(x=20, y=80)
        l3 = Label(GUI1, text="User Name").place(x=20, y=130)
        l4 = Label(GUI1, text="Password").place(x=20, y=180)

        IP = Entry(GUI1, bd=5)
        IP.place(x=140, y=30)
        PORT = Entry(GUI1, bd=5)
        PORT.place(x=140, y=80)
        UserName = Entry(GUI1, bd=5)
        UserName.place(x=140, y=130)
        Password = Entry(GUI1, bd=5, show="*")
        Password.place(x=140, y=180)

        submit_button = Button(GUI1, text="Submit", command=lambda: Decision.Submit(IP.get(), PORT.get(), UserName.get(), Password.get()))
        submit_button.place(x=20, y=215)

        GUI1.mainloop()

    def SecondWindow(self, info):
        GUI2 = Tk()
        GUI2.title("Chit Chat")
        GUI1.destroy()  # To Destroy 1st Window
        GUI2.geometry("550x600")
        GUI2.resizable(width=False, height=False)

      
        Msg_Frame = Frame(GUI2)  # 2nd Frame for Inserting Message
        Msg_Frame.pack()

        Scroll_Bar = Scrollbar(Msg_Frame)  # Scrollbar in 2nd Frame
        Display_Msg = Text(Msg_Frame, height=32, yscrollcommand=Scroll_Bar.set)  # Text Box in 2nd Frame
        Scroll_Bar.config(command=Display_Msg.yview)
        Scroll_Bar.pack(side=RIGHT, fill=Y)

        Display_Msg.pack(side=LEFT, fill=BOTH)
        Display_Msg.insert(END, "\t\t\t[*]CONNECTED[*]\n\n")
        Display_Msg.config(state=DISABLED)  # To Disable Text Box

        def DisplayMsgSent(Msg_Sent):
            Display_Msg.config(state=NORMAL)  # To Enable Text Box
            Msg_Sent = Msg_Sent + "\n"
            Display_Msg.insert(END, Msg_Sent)
            Display_Msg.pack(side=LEFT, fill=BOTH)
            Display_Msg.config(state=DISABLED)  # To Disable Text Box

        def Send(Msg_To_Send, User_Input):
            time.sleep(0.05)
            Msg_To_Send = "[" + info[2] + "]> " + Msg_To_Send
            connection.send(Encryption.Encrypt(Orginal_Key, Msg_To_Send))
            User_Input.delete(0, "end")  # To Remove Text in Entry
            DisplayMsgSent(Msg_To_Send)

        def DisplayMsgRecv(Msg_Recv):
            Display_Msg.config(state=NORMAL)  # To Enable Text Box
            time.sleep(0.05)
            Msg_Recv = Msg_Recv + "\n"
            Display_Msg.insert(END, Msg_Recv)
            Display_Msg.config(state=DISABLED)  # To Disable Text Box           

        def RecivedMsg():
            while True:
                Msg_recv = connection.recv(1024)
                DisplayMsgRecv(Encryption.Decrypt(Orginal_Key, Msg_recv))

        User_Input = Entry(GUI2, bd=5, width=40)
        User_Input.place(x=120, y=530)

        Send_Button = Button(GUI2, text="SEND", command=lambda: Send(User_Input.get(), User_Input))
        Send_Button.place(x=380, y=530)

        Thread_to_receive = threading.Thread(target=RecivedMsg)
        Thread_to_receive.start()

        def on_closing():
            # Close the database connection
        
            GUI2.destroy()

        GUI2.protocol("WM_DELETE_WINDOW", on_closing)

        GUI2.mainloop()

GUI = MainGUI()
GUI.FirstWindow()
