import time
import random
import os
import webbrowser as wb
import speech_recognition as sr
import subprocess
from tkinter import *


def recognize():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        try:
            os.system("espeak 'Listening'")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            print(text)
            return text
        except sr.UnknownValueError:
            os.system("espeak 'Sorry, I didnt get that Can you repeat it?'")
        except sr.RequestError:
            os.system("espeak 'Sorry, I cannot get an internet connection. Please connect to the internet'")


def greeting():
    os.system("espeak 'Greetings! My name is Adolin'")
    time.sleep(0.5)
    os.system("espeak 'I am a virtual assistant you can ask to do a variety of things.'")
    time.sleep(0.5)
    os.system("espeak 'Click the 'ask' button to give me a command'")


def website():
    os.system("espeak 'What would you like to search'")
    search = recognize()
    generalresponse()
    wb.open_new_tab("https://www.google.ca/search?q=" + (str(search)))


def program():
    os.system("espeak 'What program would you like to open?'")
    program = recognize()
    generalresponse()



def functions():
    answer = recognize()
    if answer.lower() == 'search web':
        website()
    if answer.lower() == 'search the web':
        website()
    if answer.lower() == 'web search':
        website()
    if answer.lower() == 'Open Program':
        program()


def generalresponse():
    responses = open('responses.txt', 'r')
    response = responses.readlines()
    y = random.randint(0, 5)
    responsefinal = response[y]
    os.system(responsefinal)


def infopanel():
    class info(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.master = master
            self.init_window()

        def init_window(self):
            self.master.title("Adolin")
            self.pack(fill=BOTH, expand=1)
            self.configure(background="gray33")
            button = Button(self, text="Possible Commands:", height=3, width=20)
            button.place(x=160, y=25)
            quitbutton = Button(self, text="exit", height=2, width=5, command=self.client_exit)
            quitbutton.place(x=229, y=400)

        def client_exit(self):
            root.destroy()

    root = Tk()
    root.geometry("500x500")
    app = info(root)
    root.mainloop()


def startinterface():
    class Window(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.master = master
            self.init_window()

        def init_window(self):
            self.master.title("Adolin")
            self.pack(fill=BOTH, expand=1)
            self.configure(background="gray33")
            quitbutton = Button(self, text="Quit", height=2, width=5, command=self.client_exit)
            quitbutton.place(x=230, y=400)
            togglebutton = Button(self, text="Activate", height=5, width=12, command=self.activate)
            togglebutton.place(x=200, y=150)

        def client_exit(self):
            exit()

        def activate(self):
            greeting()
            root.destroy()

    root = Tk()
    root.geometry("500x500")
    app = Window(root)
    root.mainloop()


def maininterface():
    class Window2(Frame):
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.master = master
            self.init_window()

        def init_window(self):
            self.master.title("Adolin")
            self.pack(fill=BOTH, expand=1)
            self.configure(background="gray33")
            quitbutton = Button(self, text="Quit", height=2, width=5, command=self.client_exit)
            quitbutton.place(x=230, y=400)
            askbutton = Button(self, text="Ask", height=8, width=30, command=self.ask)
            askbutton.place(x=125, y=100)
            informationbutton = Button(self, text="Click for Possible Commands", height=3, width=30, command=self.info)
            informationbutton.place(x=125, y=250)

        def client_exit(self):
            exit()

        def ask(self):
            functions()

        def info(self):
            infopanel()

    root = Tk()
    root.geometry("500x500")
    app = Window2(root)
    root.mainloop()


startinterface()
maininterface()
