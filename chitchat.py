def HostORConnect(self,ToDo):
        global Do
        if ToDo.get() == 1:
            Do ="Connect"
        else:
            Do = "Host"

    def Submit(self,IP,PORT,user_name,Password):
        global info,SocketNetworking
        SocketNetworking = SocketNetworking()

        if IP != "" and PORT != "" and user_name != "" and Password != "":
            info = [IP,int(PORT),user_name,Password]
            if Do == "Connect":
                Verification = SocketNetworking.Connect(info)

                if Verification == "Verified":
                    GUI.SecondWindow(info)
                else:
                    messagebox.showerror("ERROR","PASSWORD IS WRONG")
                    GUI1.destroy()
                    exit()
            else:
                Verification = SocketNetworking.Host(info)
                if Verification == "Verified":
                    GUI.SecondWindow(info)
                else:
                    messagebox.showwarning("SECURITY WARNING","ANONYMOUS PERSON IS TRYING TO LOGIN")
                    GUI1.destroy()
                    exit()

class MainGUI:

    def FirstWindow(self):
        global GUI1
        GUI1 = Tk()
        GUI1.title("Chit Chat")
        GUI1.geometry("350x250")
        GUI1.resizable(width=False,height=False)

        ToDo = IntVar()

        Decision = DecisionAndUserinfo()
        Connect=Radiobutton(GUI1,text="Connect",variable=ToDo,value = 1,command=lambda:Decision.HostORConnect(ToDo))
        Host=Radiobutton(GUI1,text="Host",variable=ToDo,value = 2,command=lambda:Decision.HostORConnect(ToDo))
        Connect.grid(row=0,column=0)
        Host.grid(row=0,column=1)

        l1 = Label(GUI1,text="Host IP").place(x=20,y=30)
        l2 = Label(GUI1,text="PORT").place(x=20,y=80)
        l3 = Label(GUI1,text="User Name").place(x=20,y=130)
        l4 = Label(GUI1,text="Password").place(x=20,y=180)

        IP = Entry(GUI1,bd=5)
        IP.place(x=140,y=30)
        PORT = Entry(GUI1,bd=5)
        PORT.place(x=140,y=80)
        UserName = Entry(GUI1,bd=5)
        UserName.place(x=140,y=130)
        Password = Entry(GUI1,bd=5,show="*")
        Password.place(x=140,y=180)

        submit_button = Button(GUI1,text="Submit",command=lambda:Decision.Submit(IP.get(),PORT.get(),UserName.get(),Password.get()))
        submit_button.place(x=20,y=215)

        GUI1.mainloop()

    def SecondWindow(self,info):
        GUI2 = Tk()
        GUI2.title("Chit Chat")
        GUI1.destroy() # To Destroy 1st Window
        GUI2.geometry("550x600")
        GUI2.resizable(width=False,height=False)

        Msg_Frame = Frame(GUI2) #2nd Frame for Inserting Message
