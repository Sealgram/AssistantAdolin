# Note that all comments are referencing the line/ lines directly above them, unless otherwise specified.
import random
import os
import webbrowser as wb
import speech_recognition as sr
import subprocess
import requests
import datetime
from tkinter import *
'''
imports all necessary modules to run this code. Some of these require pip/brew installs, see the readme.md to see which
ones. Not all functions in this code will work on a computer that is separate from my own- particularly the function
that opens programs. On another mac, this function will partially work, but if you try to tell it to open a program that
is in the list but not on that mac it will not work. On a windows computer, it will not work at all, as the paths for
programs are completely different.
'''

'''
the following function is called almost everywhere in this code, as it recognizes the user's voice and records it for
use.
'''


def recognize():
    r = sr.Recognizer()
    # defines 'r' as the recognizer function from the speech recognition module
    mic = sr.Microphone()
    # defines 'mic' as the microphone function from the speech recognition module
    with mic as source:
        # uses mic as the source for the following code
        try:
            os.system("espeak 'Listening'")
            # makes the voice inform you it is listening
            audio = r.listen(source)
            # listens to the audio using the recognizer module coming from the source, the mic (defined above)
            text = r.recognize_google(audio)
            # uses google's speech recognition api to recognize what was said.
            print(text)
            # prints what was said into the console
            return str(text)
            # returns what was said back to wherever the function was called from
        except sr.UnknownValueError:
            return 'nodice'
            # if google's speech recognition API cannot understand you, returns a string that will not activate
            # anything, triggering the bot to tell you to ask again later on in the function.
        except sr.RequestError:
            os.system("espeak 'Sorry, I cannot get an internet connection. Please connect to the internet'")
            # This catches the error if the computer is not connected to the internet, and informs you of that.


'''
The following function is very simple: it is the first function activated when the user presses 'activate' on the
Tkinter GUI, and all that happens in it is the bot introduces himself, and the reputation is reset to the neutral value.
'''


def greeting():
    os.system("espeak 'Greetings! My name is Adolin'")
    os.system("espeak 'I am a virtual assistant you can ask to do a variety of things.'")
    os.system("espeak 'Click the 'ask' button to give me a command'")
    os.system("espeak 'It would also help if you could teach me your name, by pressing the name button'")
    # The lines the bot speaks to introduce himself
    reputation = open('reputation.txt', 'w+')
    reputation.write("10")
    # File I/O code that resets the user's reputation with the bot to 10, the neutral value.


'''
The following function is the bot's responses to general sayings the user may say to the bot, such as "hello".
If the user has pressed the 'name' button and recorded their name, the bot will use their name in it's responses.
Otherwise, the bot will not include their name in it's responses. Note that if a name has been recorded in a previous
run through of the code, the bot will continue to use that name, unless you either delete it from the file or
re-record a name over it.
'''


def generalresponses(saying):
    # Takes in what the user said as a parameter so the bot can respond accordingly
    names = open('names.txt', 'r')
    namedoc = names.readlines()
    try:
        name = namedoc[0]
    except IndexError:
        name = ''
    # Finds the user's name within the text file and stores it in a local variable to be used in the code. If the first
    # line in the text file is empty, defines the name as empty quotes, which makes the bot not say anything
    if saying == 'hello' or saying == 'hi':
        os.system(f"espeak 'Hello {name}'")
        # I had to figure out how to insert a function into espeak, because I cannot end the quotes to string in a
        # function. This was not as hard a I thought- a simple solution was to put 'f' before the quotes, which then
        # makes it search for a variable within curly brackets in the string. The same method is used in many instances
        # in this code.
    elif saying == 'what is your favorite color':
        os.system(f"espeak 'I don't think your eyes can perceive it, {name}'")
    elif saying == 'why is the sky blue':
        os.system(f"espeak 'because that is the way you perceive it, {name}'")
    elif saying == 'do you like me':
        os.system(f"espeak 'of course I like you, {name}, on a professional basis'")
    # all the bot's responses to general sayings.


'''
The following function records the name of the user when they press the 'name' button, and stores it in a file for 
later use.
'''


def namerecord():
    os.system("espeak 'What is your name'")
    # Adolin asks the user what their name is
    recordname = recognize()
    # calls the recognize function and stores what the user said as 'recordname'
    names = open('names.txt', 'w+')
    names.write(recordname)
    # Opens the 'names.txt' file and stores the name the user said in the file.
    os.system("espeak 'Your name has been recorded'")
    # Informs the user that their name has in fact been recorded.


'''
The following function is the website search function, it opens a new chrome tab (or a tab on the system's default
browser) and immediately searches google based on what the user said.
'''


def website():
    os.system("espeak 'What would you like to search'")
    # Adolin asks the user what their name is
    search = recognize()
    # Calls the recognize function and stores what the user said as 'search'
    generalresponse()
    # Says a general response based on the user's current reputation
    wb.open_new_tab("https://www.google.ca/search?q=" + (str(search)))
    # Opens a new tab in the default browser and searches google based on the user's input


'''
The following function works in tandem with the "program()" function, and the text file 'applications.txt' to open a
program based on a path. This function takes in what the user said as a parameter and finds it's index in a list, then
returns the index, as it is the same as the line that the path is located on in the text file containing all the paths. 
'''


def identifyprogram(choiceprogram):
    # Function that takes choiceprogram in as it's parameter, so that it can search the list for the program specified.
    programs = [
        'VLC', 'Illustrator', 'Photoshop', 'Premiere', 'Blender', 'Books', 'Calculator', 'Calendar', 'Chess',
        'Contacts', 'Dictionary', 'Discord', 'Facetime', 'Flappy Golf', 'Google Chrome', 'Imovie', 'Mail',
        'Malwarebytes', 'Messages', 'Minecraft', 'Notes', 'Octagon', 'Photo Booth', 'PyCharm', 'Quicktime Player',
        'Reminders', 'Spotify', 'Steam', 'System Preferences', 'TextEdit', 'You Torrent', 'Twitch'
    ]
    # This list contains all of the names of programs as the speech API will read them, organized the same way as the
    # paths within the 'applications' file.
    try:
        index = programs.index(choiceprogram.title())
        return index
    # This try gets the index for the parameter 'choiceprogram', and returns it to the program() function.
    except ValueError:
        os.system("espeak 'Sorry, I cannot open that program")
    # if the value is not in the list (you requested to open a program that dosent exist or it recorded your
    # speech wrong) it tells you that it cannot open the program- you will need to ask it again.


'''
The following function is what actually contains the subprocess command to open a program based on the returned
index from the above function- all this does is reads the path from the text file and inserts it into the subprocess
command to open the desired program.
'''


def program():
    os.system("espeak 'What program would you like to open?'")
    # Asks the user what program they would like to open
    choiceprogram = recognize()
    # calls the recognize function to record the user's answer
    generalresponse()
    # responds with  a general completion response
    programchoice = identifyprogram(choiceprogram)
    # calls the previous function taking in choiceprogram as a parameter
    paths = open('applications.txt', 'r')
    pathsread = paths.readlines()
    # opens the applications text file in read format, and defines the lines as an indexed list
    subprocess.Popen(["/usr/bin/open", "-W", "-n", "-a", str(pathsread[programchoice].strip())])
    # uses the subprocess command with the desired path and the godly .strip() function (which strips blank spaces from
    # the string it is working with) to open a specified program


'''
The following function is one of the bot's personality functions- if the user uses a common insult against the bot,
it will recognize that, and respond accordingly, well also bringing down the user's 'reputation'- if the user triggers
this function enough times and the reputation goes below 10, the bot's general responses to commands will get more
reluctant and less obedient sounding.
'''


def idontlikeinsults(insult):
    # takes in the insult against the bot as a parameter, to be used in the following code.
    names = open('names.txt', 'r')
    namedoc = names.readlines()
    try:
        name = namedoc[0]
    except IndexError:
        name = ''
    # Opens the name text document and defines the name as what is recorded, except if there is no name, then defines
    # the name as nothing to the bot will not pronounce it.
    try:
        reputation = open('reputation.txt', 'r')
        rep = reputation.readlines()
        currentrep = int(rep[0].strip())
    except IndexError:
        currentrep = 10
    # opens reputation text document and defines currentrep as what the value is, with defensive programming that resets
    # it to the neutral value in event of an error, even though that should be impossible (better safe than sorry!)
    if insult == 'you suck':
        os.system(f"espeak 'That is physically impossible, {name}, as I do not possess a mouth'")
        currentrep -= 1
    elif insult == 'you are an idiot' or insult == 'you are stupid' or insult == 'you are dumb':
        os.system(f"espeak 'Im sure the same can be said about you, {name}'")
        currentrep -= 1
    elif insult == 'screw you' or insult == 'die in a hole':
        os.system(f"espeak 'That was not very nice, {name}'")
        currentrep -= 1
    # Uniquely responds to each insult/ insults and subtracts one point from the reputation value
    reputation = open('reputation.txt', 'w')
    reputation.write(str(currentrep))
    # opens the reputation text document and records the current reputation


'''
The following function is basically the flipside of the above function, it does all the same things but for compliments,
and instead of lowering the reputation, it raises it.
'''


def ilikecompliments(compliment):
    # takes the compliment to the bot as a parameter, ready to be used in the following code
    names = open('names.txt', 'r')
    namedoc = names.readlines()
    try:
        name = namedoc[0]
    except IndexError:
        name = ''
    # Opens the name text document and defines the name as what is recorded, except if there is no name, then defines
    # the name as nothing to the bot will not pronounce it.
    try:
        reputation = open('reputation.txt', 'r')
        rep = reputation.readlines()
        currentrep = int(rep[0].strip())
    except IndexError:
        currentrep = 10
    # opens reputation text document and defines currentrep as what the value is, with defensive programming that resets
    # it to the neutral value in event of an error, even though that should be impossible, as dictated above
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
        currentrep += 1
        if y == 1:
            os.system(f"espeak 'wait, I always do this. this is awkward.'")
            currentrep += 1
    elif compliment == 'good bot':
        os.system(f"espeak 'do I get a treat now, {name}'")
        currentrep += 1
    elif compliment == 'you are the best':
        os.system(f"espeak 'Thats a nice thing to say, thank you'")
        currentrep += 1
    # uniquely responds to each compliment and adds to the reputation value with each compliment, sometimes randomly
    # picking one of two responses for each unique compliment
    reputation = open('reputation.txt', 'w')
    reputation.write(str(currentrep))
    # opens the reputation text document and records the current reputation with changes based on the compliments


'''
The following function is for when you ask the bot for the weather, and it responds by using a weather API from
a website called 'openweathermap.org', and then reads the weather to you.
'''


def weather():
    api_key = "89ea3f323d661f91d8df1df3388a2163"
    # I needed to get a personal API key to be able to use the API- this one works as long as I don't try to use it
    # more than 60 times per minute. I think we're good.
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    # defines the base URL function for simplicity
    os.system("espeak 'Please tell me the name of the city you would like to get the weather for.'")
    # asks the user what city they would like to get the weather for
    city_name = recognize()
    # calls the recognize function to get the user's input
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    # builds the URL with the base URL, API key, and the user inputted city name
    response = requests.get(complete_url)
    # uses the requests module to get the return from the complete URL
    x = response.json()
    # defines the response using JSON, so that python can interpret it.
    if x["cod"] != "404":
        # if it got a response, continues with the code
        y = x["main"]
        # defines y as the main return from the JSON
        current_temperature = y["temp"]
        # gets the current temperature in kelvin from the main
        celsius = current_temperature - 273.15
        # converts the temperature to celsius from kelvin
        z = x["weather"]
        # defines z as everything from the 'weather' part of the JSON
        weather_description = z[0]["description"]
        # pulls the description of the  weather conditions from the z value
        os.system(
            f"espeak 'The temperature is {celsius:.2f} degrees celsius, and It is currently "
            f"{weather_description} in {city_name}'"
        )
        # this command makes the bot speak the temperature and weather based on the current city
    else:
        os.system("espeak 'That is not a city, please try again'")
        # if the response returned '404', it means that the city name was not in the API's list of cities, and informs
        # the user of that.


'''
The following function is a very simple function that gets the current date and time using the datetime module, and
speaks that date and time to the user.
'''


def dateandtime():
    timedate = datetime.datetime.now()
    # defines a variable as the raw date and time information from the datetime module
    speak = timedate.strftime("%Y %m %d, and the time is %H:%M")
    # formats the date and time properly under a variable called 'speak'
    os.system(f"espeak 'The current date is {speak}'")
    # speaks the date and time


'''
The following function literally runs the whole code- it is what is called when the ask button in the Tkinter window
is pressed. it takes in the user's initial command, then uses that command to call whichever command specific function
is nessisary to complete the user's desired action.
'''


def functions():
    answer = recognize()
    # calls the recognize function and save's the user's command as a parameter
    searchweb = ['search web', 'web search', 'web', 'search', 'google', 'search the web']
    openprogram = ['open program', 'open', 'program open', 'open a program', 'open an app', 'app open']
    weathercalls = ['weather', 'what is the weather', 'tell me the weather', 'find weather', 'whats the weather']
    generalsayings = ['hello', 'hi', 'what is your favorite color', 'why is the sky blue', 'do you like me']
    dontinsultme = ['you suck', 'you are an idiot', 'you are stupid', 'you are dumb', 'screw you', 'die in a hole']
    complimentme = ['you are great', 'thank you', 'thanks', 'good job', 'good bot', 'you are the best assistant']
    timedate = ['what is the time', 'what is the date', 'date', 'time', 'what is the date and time', 'time date']
    # all of these lists contain the key words and phrases that will make the bot do different things
    if str(answer).lower() in searchweb:
        website()
        # if the user's answer is in the searchweb list, calls the website function
    elif str(answer).lower() in openprogram:
        program()
        # if the user's answer is in the openprogram list, calls the program function
    elif str(answer).lower() in weathercalls:
        weather()
        # if the user's answer is in the weathercalls list, calls the weather function
    elif str(answer).lower() in generalsayings:
        generalresponses(answer)
        # if the user's answer is in the generalsayings list, calls the generalresponses function
    elif str(answer).lower() in dontinsultme:
        idontlikeinsults(answer)
        # if the user's answer is in the dontinsultme list, calls the idontlikeinsults function
    elif str(answer).lower() in complimentme:
        ilikecompliments(answer)
        # if the user's answer is in the complimentme list, calls the ilikecompliments function
    elif str(answer).lower() in timedate:
        dateandtime()
        # if the user's answer is in the timedate list, calls the dateandtime function
    else:
        os.system(f"espeak 'i am sorry, I didnt get that, please ask again'")
        # if the user's answer is not in any of the lists, or the recognizer did not recognize what
        # the user said, tells them to ask again.


'''
This next function is the generalresponse function, which makes the bot give the user a general response based on what
their reputation is, from a text file containing all the possible responses.
'''


def generalresponse():
    responses = open('responses.txt', 'r')
    response = responses.readlines()
    # opens the responses text file and defines it as a list of all the lines in the file
    try:
        reputation = open('reputation.txt', 'r')
        rep = reputation.readlines()
        returnrep = int(rep[0].strip())
    except IndexError:
        returnrep = 10
    # opens reputation text document and defines returnrep as what the value is, with defensive programming that resets
    # it to the neutral value in event of an error, even though that should be impossible, but python is sneaky
    if returnrep == 10:
        y = random.randint(0, 5)
        responsefinal = response[y]
        os.system(responsefinal)
        # if the reputation is the neutral value (10), reads the user one of the neutrally helpful responses
    elif returnrep < 10:
        y = random.randint(7, 12)
        responsefinal = response[y]
        os.system(responsefinal)
        # if the reputation is below the neutral value (10), reads the user one of the negatively helpful responses
    elif returnrep > 10:
        y = random.randint(14, 19)
        responsefinal = response[y]
        os.system(responsefinal)
        # if the reputation is above the neutral value (10), reads the user one of the positively helpful responses


'''
The following function is the first of my 3 Tkinter window functions, and this one is the least important- it shows
the user a (non-exhaustive) list of possible commands that they can ask the bot. Each command appears as a button,
but they are non-functional, as you need to click the ask button and communicate with the bot to be able to do stuff.
'''


def infopanel():
    class info(Frame):
        # the class the Tkinter window is contained inside
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.master = master
            self.init_window()
            # the init function the Tkinter window

        def init_window(self):
            # the function that contains all the information and commands for said Tkinter window
            self.master.title("Adolin")
            # specifying a name for the window
            self.pack(fill=BOTH, expand=1)
            # packing the window so it can be filled
            self.configure(background="gray33")
            # changes the window background to a gray variant
            button = Button(self, text="Possible Commands:", height=3, width=30)
            button.place(x=125, y=25)
            # makes and places a non-functional button containing information
            webbutton = Button(self, text="Search Web", height=3, width=22)
            webbutton.place(x=160, y=100)
            # makes and places a non-functional button containing information
            programbutton = Button(self, text="Open a Program", height=3, width=22)
            programbutton.place(x=160, y=175)
            # makes and places a non-functional button containing information
            weatherbutton = Button(self, text='Whats the Weather', height=3, width=22)
            weatherbutton.place(x=160, y=250)
            # makes and places a non-functional button containing information
            datetimebutton = Button(self, text='What is the date and time', height=3, width=22)
            datetimebutton.place(x=160, y=325)
            # makes and places a non-functional button containing information
            quitbutton = Button(self, text="exit", height=2, width=5, command=self.client_exit)
            quitbutton.place(x=229, y=400)
            # makes and places a button that allows you to exit the window

        def client_exit(self):
            root.destroy()
            # the function that is called when the 'exit' button is pressed

    root = Tk()
    root.geometry("500x500")
    app = info(root)
    root.mainloop()
    # activating the Tkinter window and specifying it's size


'''
The following function is the second of my 3 Tkinter window functions, and this one is the second most important- it
it the first one that you see, and it contains the activate button, which triggers the greeting() function- basically
the bot will introduce itself and ask you to record your name by pressing a button in the main window, then it will
close this window and activate the main window.
'''


def startinterface():
    class Window(Frame):
        # the class the Tkinter window is contained inside
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.master = master
            self.init_window()
            # the init function the Tkinter window

        def init_window(self):
            # the function that contains all the information and commands for said Tkinter window
            self.master.title("Adolin")
            # specifying a name for the window
            self.pack(fill=BOTH, expand=1)
            # packing the window so it can be filled
            self.configure(background="gray33")
            # changes the window background to a gray variant
            quitbutton = Button(self, text="Quit", height=2, width=5, command=self.client_exit)
            quitbutton.place(x=230, y=400)
            # creating and placing a button that allows the user to quit the interface, which will stop the code
            togglebutton = Button(self, text="Activate", height=5, width=12, command=self.activate)
            togglebutton.place(x=200, y=150)
            # creating and placing a button that allows the user to toggle the greeting function and activate the  code

        def client_exit(self):
            exit()
            # function for when the quit button is pressed

        def activate(self):
            greeting()
            root.destroy()
            # function for when the activate button is pressed (greeting function runs, then this window closes).

    root = Tk()
    root.geometry("500x500")
    app = Window(root)
    root.mainloop()
    # activating the Tkinter window and specifying it's size


'''
This is the final Tkinter window, and the most important of the three, as it is the one containing the 'ask' button.
When the ask button is pressed, the bot listens to what you say to it and responds accordingly. This window also
contains three other buttons- 'quit', 'name' and 'possible commands'. The 'quit' button is pretty self explanatory
(quits the code and closes the Tkinter window), the name button activates the name function and records the user's 
name in a text file, and the 'possible commands' button activates the first tkinter window, which displays a list of 
possible commands.
'''


def maininterface():
    class Window2(Frame):
        # The class that the Tkinter window is contained inside
        def __init__(self, master=None):
            Frame.__init__(self, master)
            self.master = master
            self.init_window()
            # The init function for the Tkinter window

        def init_window(self):
            # The function that contains all the commands and content for said window
            self.master.title("Adolin")
            # Giving the window a name
            self.pack(fill=BOTH, expand=1)
            # packing the window so it can be filled
            self.configure(background="gray33")
            # changing the window's background to a variant of grey
            quitbutton = Button(self, text="Quit", height=2, width=5, command=self.client_exit)
            quitbutton.place(x=230, y=400)
            # creating and placing a button that quits the code and exits the window
            namebutton = Button(self, text="Name", height=2, width=5, command=self.name)
            namebutton.place(x=230, y=350)
            # creating and placing a button that calls a function which records the user's name
            askbutton = Button(self, text="Ask", height=8, width=30, command=self.ask)
            askbutton.place(x=125, y=100)
            # creating and placing the fabled ask button which is the pathway for communicating with the bot
            informationbutton = Button(self, text="Click for Possible Commands", height=3, width=30, command=self.info)
            informationbutton.place(x=125, y=250)
            # creating and placing the information panel button

        def client_exit(self):
            exit()
            # Function for when the exit button is pressed

        def ask(self):
            functions()
            # function for when the ask button is pressed

        def info(self):
            infopanel()
            # function for when the info button is pressed

        def name(self):
            namerecord()
            # function for when the name button is pressed

    root = Tk()
    root.geometry("500x500")
    app = Window2(root)
    root.mainloop()
    # activating the Tkinter window and specifying it's size


startinterface()
maininterface()
# calling the startinterface function and the maininterface function in order, when the python file is run
