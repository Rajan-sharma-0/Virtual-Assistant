

import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import smtplib
import sys






engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 160)

# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
# Function to convert speech to text
def take_command():

    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source, timeout=7, phrase_time_limit=10)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Can you repeat?")
        return "None"
    except sr.RequestError:
        speak("Sorry, I'm unable to process your request right now.")
        return "None"
    return query.lower()

# Greet the use
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

    speak("I am Nova. How can I help you?")

# To sand E-mail
def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com', 534)
    server.ehlo()
    server.starttls()
    server.login('rajankumarsharma543321@gmail.com', 'clashofclan')
    server.sendmail('nk800109@gmail.com', to, content)
    server.close()

if __name__ == "__main__":
    greet()
    while True:
    # if 1:
        query = take_command()
        # Task execution logic
        if "open notepad" in query:
            notepad_path = "C:\\Windows\\System32\\notepad.exe"  # Update with correct path
            os.startfile(notepad_path)
        elif "open chrome" in query:
            chrome_peth = "C:\\Users\\rsach\\OneDrive\\Documents\\OneDrive\\Desktop\\Rajan - Chrome.lnk"
            os.startfile(chrome_peth)

        elif "open vs code" in query:
            vs_code_peth = "C:\\Users\\rsach\\OneDrive\\Documents\\OneDrive\\Desktop\\Visual Studio Code.lnk"
            os.startfile(vs_code_peth)

        elif "open youtube" in query:
            chrome_path = "C:\\Users\\rsach\\OneDrive\\Documents\\OneDrive\\Desktop\\YouTube.lnk"  # Update with correct path
            os.startfile(chrome_path)

        elif "open command prompt" in query:
            os.system("start cmd")
## open Camera
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                speak("Unable to access the camera. Please check if it is connected properly.")
            else:
                while True:
                    ret, img = cap.read()
                    if not ret:
                        speak("Error capturing frame from the camera.")
                        break
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:  # 'ESC' key
                        break
                cap.release()
                cv2.destroyAllWindows()

## Play Music
        elif "play music" in query:
            music_dir = "D:\\Downloads\\music"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir, rd))
## IP Address
        elif "ip address" in query:
            ip = get('https://api.ipify.org/').text
            speak(f"your IP address is {ip}")


## Wikipedia
        elif "what is " in query:
            speak("Searching.py wikipedia....")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("according to wikipedia")
            speak(results)
            # print(results)


## Google
        elif "open google" in query:
            speak("sir, what should i search on google")
            cm = take_command().lower()
            webbrowser.open(f"{cm}")

##To sand E-mail
        elif "email " in query:
            try:
                speak("what should i say?")
                content = take_command().lower()
                to = "nk800109@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent to rajan")

            except Exception as e:
                print(e)
                speak("sorry sir, i am not able to sent this mail to rajan")

        elif "no thanks" in query:
            speak("thanks for using me sir , have a good day")
            sys.exit()
        elif "stop" in query:
            speak("thanks for using me sir , have a good day")
            sys.exit()

        # speak("sir, do you have any other work")



