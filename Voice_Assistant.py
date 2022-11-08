# importing required module
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from sys import exit
from tkhtmlview import HTMLLabel
import pyttsx3 as tts  # Library for converting text to speech
import speech_recognition as stt  # Library for converting speech to text
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import datetime

import shutil

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

engine = tts.init('sapi5')  # sapi5 is the microsoft tts tool
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # id 1 is for female voice and 0 is for male voice

# create tkinter window
root = tk.Toplevel()

load = Image.open("va.png")
load2 = Image.open("va2.jpg")
render = ImageTk.PhotoImage(load)
render2 = ImageTk.PhotoImage(load2)
img = Label(root, image=render)
img2 = Label(root, image=render2)
img.place(x=900, y=450)
img2.place(x=40, y=450)


def play():
    # Using the below function for the AI to speak
    def speak(text):
        engine.say(text)
        engine.runAndWait()

    def wishMe():
        hour = datetime.datetime.now().hour  # Setting the time
        if 7 <= hour <= 12:
            speak("Good Morning")
            print("Good Morning")
        if 12 < hour <= 17:
            speak("Good Afternoon")
            print("Good Afternoon")
        if 17 < hour <= 22:
            speak("Good Evening")
            print("Good Evening")

    def takeCommand():
        r = stt.Recognizer()  # Setting up a recognizer
        with stt.Microphone() as source:  # Making the microphone that I am on as a source
            print("Talk now....")
            speak("Talk now")
            audio = r.listen(source)  # Listening the audio I am inputting through the microphone

            try:
                statement = r.recognize_google(audio, language='en-us')
                print('You said "{}"\n'.format(statement))

            except Exception as e:
                print("Pardon me, could you please say that again")
                speak("Pardon me, could you please say that again")
                takeCommand()  # Calling the function in a recursive manner in the case of error
                return "None"
            speak(statement)
            return statement

    wishMe()
    speak("I am Emma, your personal assistant")
    print("I am Emma, your personal assistant")
    print("Tell me what you want to do")
    speak("Tell me what you want to do")

    print("1.Play youtube\n2.Lookup something in wikipedia\n3.Search something on Google\n4.Display Time\n5.Display "
          "Date\n6.Copy File\n7.screenshot \n8.education")

    user_choice_variable = takeCommand()
    print(user_choice_variable)

    if (user_choice_variable == "youtube") or (user_choice_variable == "YouTube"):
        speak("Opening youtube...")
        print("Opening youtube...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.youtube.com/")

        print("Tell me what you want to play")
        speak("Tell me what you want to play")

        searchBox = driver.find_element(By.XPATH,
                                        "/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div[1]/div[1]/input")

        searchElement = takeCommand()
        searchBox.send_keys(searchElement)

        searchButton = driver.find_element(By.XPATH,
                                           "/html/body/ytd-app/div[1]/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/button/yt-icon")
        searchButton.click()

        driver.get('https://www.youtube.com/results?search_query={}'.format(searchElement))

        playVideo = driver.find_element(By.ID, "video-title")
        speak("Playing {}".format(searchElement))
        playVideo.click()

    elif (user_choice_variable == "wikipedia") or (user_choice_variable == "Wikipedia"):
        speak("Opening wikipedia...")
        print("Opening wikipedia...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://en.wikipedia.org/wiki/Main_Page")

        print("Enter what you want to search")
        speak("Enter what you want to search")
        user_input = takeCommand()

        search_box = driver.find_element(By.XPATH, "/html/body/div[5]/div[1]/div[2]/div/div/form/div/input[1]")

        search_box.send_keys(user_input)
        search_box.submit()

    elif (user_choice_variable == "google") or (user_choice_variable == "Google"):
        speak("Opening Google...")
        print("Opening Google...")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get("https://www.google.co.in/")
        print("Tell me you want to search")
        speak("Tell me you want to search")
        search_Talk = takeCommand()

        google_search = driver.find_element(By.XPATH,
                                            "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")

        google_search.send_keys(search_Talk)

        google_search.submit()

    elif (user_choice_variable == "time") or (user_choice_variable == "Time"):
        t = datetime.datetime.now().time()
        print("Time is {}".format(t))
        speak("Time is {}".format(t))

    elif (user_choice_variable == "date") or (user_choice_variable == "Date"):
        d = datetime.datetime.now().date()
        print("Date is {}".format(d))
        speak("Date is {}".format(d))

    elif (user_choice_variable == "copy file") or (user_choice_variable == "Copy File"):
        speak("Enter the location of the file")
        print("Enter the location of the file")
        source = input()

        speak("Enter the destination of the file")
        print("Enter the destination of the file")
        destination = input()

        try:
            shutil.copyfile(source, destination)
            print("File copied successfully.")

        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        # If destination is a directory.
        except IsADirectoryError:
            print("Destination is a directory.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        # For other errors
        except:
            print("Error occurred while copying file.")

    elif (user_choice_variable == "screenshot") or (user_choice_variable == "Screenshot"):
        speak('Please go on the screen whose screenshot you want to take, after 5 seconds I will take screenshot')
        print('Please go on the screen whose screenshot you want to take, after 5 seconds I will take screenshot')

        speak('Taking screenshot....3........2.........1.......')
        print('Taking screenshot....3........2.........1.......')
        pyautogui.screenshot('screenshot_by_sysaa.png')
        speak('The screenshot is saved as screenshot_by_sysaa.png')
        print('The screenshot is saved as screenshot_by_sysaa.png')

    elif (user_choice_variable == "education") or (user_choice_variable == "Education"):
        speak("Opening the IEEE site...")
        print("Opening the IEEE site...")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://sci-hub.hkvisa.net/")

    else:
        print("Sorry the feature is not available yet...")
        speak("Sorry the feature is not available yet")
        print("Do you want to execute another instruction")
        speak("Do you want to execute another instruction")
        answer = takeCommand()
        if answer == "yes":
            print("Please ru-run the program")
            speak("Please ru-run the program")
        else:
            exit()


my_label = HTMLLabel(root, html="<section = 'header'>\
            <h1>Welcome</h1>\
            <p>This is a voice assistant build by us, which can do the following functions:\
                <br/>\
                <p>(What has to be said is indicated by bold letters)</p>\
            </p>\
            <br/>\
            <ol>\
                <b><li></b>Play <b>Youtube</b></li><br/>\
                <b><li></b>Lookup something in <b>Wikipedia</b></li><br/>\
                <b><li></b>Search something on <b>Google</b></li><br/>\
                <b><li></b>Display <b>Time</b></li><br/>\
                <b><li></b>Display <b>Date</b></li><br/>\
                <b><li></b>Open <b>Health</b></li><br/>\
                <b><li></b>Take a <b>Screenshot</b></li>\
                <b><li></b>IEEE <b>Education</b></li>\
                </ol>\
                </section>")

my_label.pack(side="top")

# create a button which holds
# our play function using command = play
btn = Button(root, text="Speak",
             width="15", pady=10,
             font="bold, 15",
             command=play, bg='yellow')

btn.place(x=900,
          y=900)
# btn.pack(side="bottom")


# give a title
root.title("Emma")

# we can not change the size
# if you want you can change
root.geometry("1920x1080")
# start the gui
root.mainloop()