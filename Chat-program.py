from tkinter import *
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from ast import literal_eval
from webbrowser import get


class Chat:
    def __init__(self):

        self.VERSION = 0.99
        self.BACKGROUND = '#141414'
        self.FOREGROUND = '#FFFFFF'
        self.THEME = '#FFFFFF'

        self.connectionIP = 'chat-sv.ddns.net'
        self.connectionPort = 6666
        self.colourIndex = 0

        self.Session = Network(self.connectionIP, self.connectionPort, self)
        self.Colours = ['#f1c40f', '#2ecc71', '#3498db', '#9b59b6', '#e74c3c']
        self.Names = ['Yellow', 'Green', 'Blue', 'Purple', 'Red']
        self.Username = None

        self.showingInformation = False
        self.openingLinks = False

        self.Window = Tk()
        self.Window.geometry('800x350')
        self.Window.config(bg=self.BACKGROUND)
        self.Window.title(f'Messenger - Version {self.VERSION}')

        self.Frame_Login = Frame(self.Window, bg=self.BACKGROUND)
        self.Frame_Chat = Frame(self.Window, bg=self.BACKGROUND)
        self.Frame_Advanced = Frame(self.Window, bg=self.BACKGROUND)

        self.Label_Username = Label(self.Frame_Login, text='USERNAME', font=('Verdana', 20 , 'bold'), fg=self.BACKGROUND, bg=self.FOREGROUND).place(relx=.05, rely=.25)
        self.Entry_Username = Entry(self.Frame_Login, width=50, font=('Courier New', 20 , 'bold'), bg=self.BACKGROUND, fg=self.FOREGROUND, bd=0, insertbackground='#FFFFFF')

        self.Button_Information = Button(self.Frame_Login, text='More Information', font=('MS PGothic', 12, 'bold'), fg='#bdc3c7', bg=self.BACKGROUND, bd=0, command=lambda: self.toggle()).place(relx=.05, rely=.75)
        self.Button_Colour = Button(self.Frame_Login, text='Yellow', font=('MS PGothic', 12, 'bold'), fg='#f1c40f', bg=self.BACKGROUND, bd=0, command=lambda: self.cycle())
        self.Button_Connect = Button(self.Frame_Login, text='Connect to Server', font=('MS PGothic', 12, 'bold'), fg='#2ecc71', bg=self.BACKGROUND, bd=0, command=lambda: self.connect()).place(relx=.76, rely=.75)

        self.Label_Notification = Label(self.Frame_Login, text='', font=('MS PGothic', 12 , 'bold'), bg=self.BACKGROUND, fg='#E74C3C', width=71, anchor='e')
        self.Label_IP = Label(self.Frame_Advanced, text='Connection IP', font=('MS PGothic', 12 , 'bold'), bg=self.BACKGROUND, fg='#bdc3c7', width=20, anchor='e').place(relx=.05, rely=.35)
        self.Label_Port = Label(self.Frame_Advanced, text='Connection Port', font=('MS PGothic', 12 , 'bold'), bg=self.BACKGROUND, fg='#bdc3c7', width=20, anchor='e').place(relx=.05, rely=.5)
        self.Label_Timeout = Label(self.Frame_Advanced, text='Timeout in Seconds', font=('MS PGothic', 12 , 'bold'), bg=self.BACKGROUND, fg='#bdc3c7', width=20, anchor='e').place(relx=.05, rely=.65)
        self.Label_Commands = Label(self.Frame_Advanced, text='Using Commands', font=('MS PGothic', 12 , 'bold'), bg=self.BACKGROUND, fg='#bdc3c7', width=20, anchor='e').place(relx=.05, rely=.8)
        self.Label_Info_IP = Label(self.Frame_Advanced, text=f'{self.connectionIP}', font=('MS PGothic', 12 , 'bold'), bg='WHITE', fg='#141414', width=15, anchor='e').place(relx=.55, rely=.35)
        self.Label_Info_Port = Label(self.Frame_Advanced, text=f'{self.connectionPort}', font=('MS PGothic', 12 , 'bold'), bg='WHITE', fg='#141414', width=15, anchor='e').place(relx=.55, rely=.5)
        self.Label_Info_Timeout = Label(self.Frame_Advanced, text=f'No Timeout', font=('MS PGothic', 12 , 'bold'), bg='WHITE', fg='#141414', width=15, anchor='e').place(relx=.55, rely=.65)
        self.Label_Info_Commands = Label(self.Frame_Advanced, text=f'Enabled', font=('MS PGothic', 12 , 'bold'), bg='WHITE', fg='#141414', width=15, anchor='e').place(relx=.55, rely=.8)

        self.Label_Header =  Label(self.Frame_Chat, text='_' * 103, font=('MS PGothic', 16, 'bold'), fg=self.Colours[self.colourIndex], bg=self.BACKGROUND)
        self.Label_Header.place(relx=.05, rely=.075)
        self.Label_Title = Label(self.Frame_Chat, text=self.Username, font=('MS PGothic', 16, 'bold'), fg=self.FOREGROUND, bg=self.BACKGROUND)
        self.Label_Title.place(relx=.05, rely=.05)
        self.Box_Chat = Text(self.Frame_Chat, font=('Courier New', 11, 'bold'), fg=self.FOREGROUND, bg=self.BACKGROUND, width=79, height=11, bd=4)
        self.Box_Chat.place(relx=.054, rely=.15)
        self.Entry_Message = Entry(self.Frame_Chat, width=73, font=('Courier New', 11, 'bold'))
        self.Entry_Message.place(relx=.054, rely=.65)
        self.Button_Send = Button(self.Frame_Chat, text='Send', font=('MS PGothic', 12, 'bold'),fg=self.Colours[self.colourIndex], bg=self.BACKGROUND, bd=0, command=lambda: self.message())
        self.Button_Send.place(relx=.89, rely=.65)
        self.Button_Disconnect = Button(self.Frame_Chat, text='Disconnect', font=('MS PGothic', 12, 'bold'), fg='#E74C3C', bg=self.BACKGROUND, bd=0, command=lambda: self.disconnect()).place(relx=.05, rely=.75)
        self.Button_Change = Button(self.Frame_Chat, text='Change Username', font=('MS PGothic', 12, 'bold'), fg='#bdc3c7', bg=self.BACKGROUND, bd=0, command=lambda: self.change()).place(relx=.2, rely=.75)
        self.Button_Links = Button(self.Frame_Chat, text='Allow Links', font=('MS PGothic', 12, 'bold'), fg='#f39c12', bg=self.BACKGROUND, bd=0, command=lambda: self.block())

        self.Button_Colour.place(relx=.25, rely=.75)
        self.Button_Links.place(relx=.41, rely=.75)

        self.Label_Notification.place(relx=.056, rely=.65)

        self.Entry_Username.place(relx=.05, rely=.4)
        self.Entry_Username.bind('<Return>', lambda event: self.connect())

        self.Entry_Message.bind('<Return>', lambda event: self.message())

        self.Frame_Login.place(relx=0, rely=0, width=800, height=400)

        self.Entry_Username.focus()

        self.Window.mainloop()

    def disconnect(self):
        self.Session.stop()
        self.Session = Network(self.connectionIP, self.connectionPort, self)
        self.Frame_Chat.place_forget()
        self.Frame_Login.place(relx=0, rely=0, width=800, height=400)

    def change(self):
        self.show('Change Username: Feature is currently unavailable', '#95a5a6')

    def message(self):
        self.Session.send(str({'data-type': 'chat', 'message': self.Entry_Message.get(), 'user': self.Username, 'colour': self.Colours[self.colourIndex]}))
        self.Entry_Message.delete(0, END)

    def show(self, message, colour):
        self.Box_Chat.tag_config(colour, foreground=colour, underline=0)
        self.Box_Chat.insert(INSERT ,'\n' + message, colour)

    def url(self, link):
        if self.openingLinks:
            get("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s").open(link)

    def block(self):
        self.openingLinks = not self.openingLinks
        if self.openingLinks:
            self.Button_Links.config(fg='#2ecc71')
            self.show('Allow Links: URLs that are sent in chat will now automatically open in Google  Chrome.', '#95a5a6')
        else:
            self.Button_Links.config(fg='#f39c12')
            self.show('Allow Links: URLs will no longer be automatically opened.', '#95a5a6')

    def cycle(self):
        self.colourIndex += 1
        if self.colourIndex == 4:
            self.colourIndex = 0
        self.Button_Colour.config(text=self.Names[self.colourIndex], fg=self.Colours[self.colourIndex])
        self.Label_Header.config(fg=self.Colours[self.colourIndex])
        self.Button_Send.config(fg=self.Colours[self.colourIndex])

    def toggle(self):
        self.showingInformation = not self.showingInformation
        if self.showingInformation:
            self.Frame_Advanced.place(relx=.437, rely=.15, width=450, height=200)
        else:
            self.Frame_Advanced.place_forget()

    def connect(self):
        if len(self.Entry_Username.get()) != 0:
           if self.Session.start():
               self.Frame_Login.place_forget()
               self.Frame_Advanced.place_forget()
               self.Username = self.Entry_Username.get()
               self.Frame_Chat.place(relx=0, rely=0, width=800, height=400)
               self.Label_Title.config(text=self.Username)
           else:
               self.showingInformation = False
               self.toggle()
               self.Label_Notification.config(text='Could not connect to the chat server, ensure that the address is correct.')


class Network:
    def __init__(self, address, port, main):
        self.connectionIP = address
        self.connectionPort = port
        self.mainInstance = main
        self.activeConnection = True
        self.playerUsername = None

        self.chatSocket = socket(AF_INET, SOCK_STREAM)

        self.listeningThread = Thread(target=self.listen)

    def start(self):
        if self.connect():
            self.listeningThread.start()
            return True
        return False

    def connect(self):
        try:
            self.chatSocket.connect((self.connectionIP, self.connectionPort))
            return True
        except:
            return False

    def listen(self):
        while self.activeConnection:
            try:
                receivedData = self.chatSocket.recv(150).decode()
            except:
                receivedData = None
            if receivedData:
                try:
                    sessionData = literal_eval(receivedData)
                except Exception:
                    continue
                if sessionData['data-type'] == 'chat':
                    self.mainInstance.show(f'{sessionData["user"]}: {sessionData["message"]}', sessionData['colour'])
                    if 'https://' in sessionData["message"] or 'http://' in sessionData["message"]:
                        self.mainInstance.url(sessionData["message"])
                elif sessionData['data-type'] == 'broadcast':
                    self.mainInstance.show(f'{sessionData["user"]} joined the server')

    def send(self, message):
        self.chatSocket.send(str.encode(message))

    def stop(self):
        self.activeConnection = False
        self.chatSocket.shutdown(1)
        self.chatSocket.close()

if __name__ == '__main__':
    Test = Chat()