import random
import os
import webbrowser as wb
import speech_recognition as sr
import subprocess
import requests
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
            return str(text)
        except sr.UnknownValueError:
            os.system("espeak 'Sorry, I didnt get that Can you repeat it?'")
        except sr.RequestError:
            os.system("espeak 'Sorry, I cannot get an internet connection. Please connect to the internet'")


def greeting():
    os.system("espeak 'Greetings! My name is Adolin'")
    os.system("espeak 'I am a virtual assistant you can ask to do a variety of things.'")
    os.system("espeak 'Click the 'ask' button to give me a command'")
    reputation = open('reputation.txt', 'w+')
    reputation.write("1")


def generalresponses(saying):
    names = open('names.txt', 'r')
    namedoc = names.readlines()
    try:
        name = namedoc[0]
    except IndexError:
        name = ''
    if saying == 'hello' or saying == 'hi':
        os.system(f"espeak 'Hello {name}'")
    elif saying == 'what is your favorite color':
        os.system(f"espeak 'I don't think your eyes can perceive it, but it is beautiful, {name}")
    elif saying == 'why is the sky blue':
        os.system(f"espeak 'because that is the way you perceive it, {name}")
    elif saying == 'do you like me':
        os.system(f"espeak 'of course I like you, {name}, on a professional basis")


def namerecord():
    os.system("espeak 'What is your name'")
    recordname = recognize()
    names = open('names.txt', 'w+')
    names.write(recordname)
    os.system("espeak 'Your name has been recorded.'")


def website():
    os.system("espeak 'What would you like to search'")
    search = recognize()
    generalresponse()
    wb.open_new_tab("https://www.google.ca/search?q=" + (str(search)))


def identifyprogram(choiceprogram):
    programs = [
        'VLC', 'Illustrator', 'Photoshop', 'Premiere', 'Blender', 'Books', 'Calculator', 'Calendar', 'Chess',
        'Contacts', 'Dictionary', 'Discord', 'Facetime', 'Flappy Golf', 'Google Chrome', 'Imovie', 'Mail',
        'Malwarebytes', 'Messages', 'Minecraft', 'Notes', 'Octagon', 'Photo Booth', 'PyCharm', 'Quicktime Player',
        'Reminders', 'Spotify', 'Steam', 'System Preferences', 'TextEdit', 'You Torrent', 'Twitch'
    ]
    try:
        index = programs.index(choiceprogram.title())
        return index
    except ValueError:
        os.system("espeak 'Sorry, I cannot open that program")


def program():
    os.system("espeak 'What program would you like to open?'")
    choiceprogram = recognize()
    generalresponse()
    programchoice = identifyprogram(choiceprogram)
    paths = open('applications.txt', 'r')
    pathsread = paths.readlines()
    subprocess.Popen(["/usr/bin/open", "-W", "-n", "-a", str(pathsread[programchoice].strip())])


def idontlikeinsults(insult):
    names = open('names.txt', 'r')
    namedoc = names.readlines()
    try:
        name = namedoc[0]
    except IndexError:
        name = ''
    try:
        reputation = open('reputation.txt', 'w+')
        rep = reputation.readlines()
        currentrep = int(rep[0])
    except IndexError:
        currentrep = 1
    if insult == 'you suck':
        os.system(f"espeak 'you swallow, {name}'")
        currentrep -= 1
    elif insult == 'youre an idiot' or insult == 'youre stupid' or insult == 'you are dumb':
        os.system(f"espeak 'I'm sure the same can be said about you, {name}'")
        currentrep -= 1
    elif insult == 'screw you' or insult == 'die in a hole':
        os.system(f"espeak 'That was not very nice, {name}'")
        currentrep -= 1
    reputation.write(str(currentrep))


def ilikecompliments(compliment):
    names = open('names.txt', 'r')
    namedoc = names.readlines()
    try:
        name = namedoc[0]
    except IndexError:
        name = ''
    try:
        reputation = open('reputation.txt', 'w+')
        rep = reputation.readlines()
        currentrep = int(rep[0])
    except IndexError:
        currentrep = 1
    if compliment == 'you are great':
        os.system(f"espeak 'so are you, {name}'")
        currentrep += 1
    elif compliment == 'thank you' or compliment == 'thanks':
        y = random.randint(0, 2)
        thankresponses = [f"espeak'youre welcome, {name}'", f"espeak 'No, thank you'", f"espeak 'No problem, {name}"]
        os.system(thankresponses[y])
        currentrep += 1
    elif compliment == 'good job':
        y = random.randint(0, 1)
        goodresponses = [f"espeak 'well, that is high praise, {name}'", f"espeak 'you too'"]
        os.system(goodresponses[y])
        if y == 1:
            os.system(f"espeak 'wait, I always do this. this is awkward.'")
        currentrep += 1
    elif compliment == 'good bot':
        os.system(f"espeak 'do I get a treat now, {name}'")
        currentrep += 1
    elif compliment == 'you are the best':
        os.system(f"espeak 'Thats a nice thing to say, thank you'")
        currentrep += 1


def weather():
    api_key = "89ea3f323d661f91d8df1df3388a2163"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    os.system("espeak 'Please tell me the name of the city you would like to get the weather for.'")
    city_name = recognize()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        celsius = current_temperature - 273.15
        z = x["weather"]
        weather_description = z[0]["description"]
        os.system(
            f"espeak 'The temperature is {celsius:.2f} degrees celsius, and It is currently "
            f"{weather_description} in {city_name}'"
        )


def functions():
    answer = recognize()
    searchweb = ['search web', 'web search', 'web', 'search', 'google', 'search the web']
    openprogram = ['open program', 'open', 'program open', 'open a program', 'open an app', 'app open']
    weathercalls = ['weather', 'what is the weather', 'tell me the weather', 'find weather', 'whats the weather']
    generalsayings = ['hello', 'hi', 'what is your favorite color', 'why is the sky blue', 'do you like me']
    dontinsultme = ['you suck', 'youre an idiot', 'youre stupid', 'you are dumb', 'screw you', 'die in a hole']
    complimentme = ['You are great', 'thank you', 'thanks', 'good job', 'good bot', 'you are the best assistant']
    if str(answer.lower()) in searchweb:
        website()
    elif str(answer.lower()) in openprogram:
        program()
    elif str(answer.lower()) in weathercalls:
        weather()
    elif str(answer.lower()) in generalsayings:
        generalresponses(answer)
    elif str(answer.lower()) in dontinsultme:
        idontlikeinsults(answer)
    elif str(answer.lower()) in complimentme:
        ilikecompliments(answer)


def generalresponse():
    responses = open('responses.txt', 'r')
    response = responses.readlines()
    reputation = open('reputation.txt', 'r')
    reputationvalue = reputation.readlines()
    returnrep = int(reputationvalue[0])
    if returnrep == 1:
        y = random.randint(0, 5)
        responsefinal = response[y]
        os.system(responsefinal)
    elif returnrep < 1:
        y = random.randint(7, 12)
        responsefinal = response[y]
        os.system(responsefinal)
    elif returnrep > 1:
        y = random.randint(14, 19)
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
            namebutton = Button(self, text="Name", height=2, width=5, command=self.name)
            namebutton.place(x=230, y=350)
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

        def name(self):
            namerecord()

    root = Tk()
    root.geometry("500x500")
    app = Window2(root)
    root.mainloop()


startinterface()
maininterface()
