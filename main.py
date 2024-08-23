import pyautogui
import pyttsx3
import speech_recognition as sr
import datetime
import time
import os
import cv2
import random

from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import pyjokes
import pyautogui





engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)

# Text to speech
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()
# Function to convert speech to text
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source, timeout=5, phrase_time_limit=10)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
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
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    # current_date = datetime.datetime.now().strftime("%B %d")

    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak(f"Good evening! ")

    speak(f"It is {current_time} ")
    speak("Hello sir. How can I help you?")


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

# # conversation
        if "hello" in query:
             speak("Hello sir, how are you ?")
        elif " fine" in query:
             speak("that's great, sir")
        elif "how are you" in query:
                speak("Perfect, sir")
        elif "thank you" in query:
                speak("you are welcome, sir")
        elif "what is your name" in query:
                speak("My name is nova, I am your virtual assistant")
        elif "do you know me" in query:
                speak("yes sir, I know you. your name is rajan")
        elif "do you know my friends name" in query:
                speak("ofcourse sir,")



    # Task execution logic
        if "open notepad" in query :
            notepad_path = "C:\\Windows\\System32\\notepad.exe"  # Update with correct path
            os.startfile(notepad_path)

        elif "close notepad" in query:
            speak("okay sir, closing notpad")
            os.system("taskkill /f /im notepad.exe")
# # chrome
        elif "open chrome" in query:
            chrome_peth = "C:\\Users\\rsach\\OneDrive\\Documents\\OneDrive\\Desktop\\Rajan - Chrome.lnk"
            os.startfile(chrome_peth)
        elif "close chrome" in query:
             speak("okay sir, closing chrome")
             os.system("taskkill /f /im chrome.exe")
# # Open vs code
        elif "open vs code" in query:
            vs_code_peth = "C:\\Users\\rsach\\OneDrive\\Documents\\OneDrive\\Desktop\\Visual Studio Code.lnk"
            os.startfile(vs_code_peth)
# close vs code
        elif "close vs code" in query:
            speak("ok sir, closing vs code")
            os.system("taskkill /f /im Code.exe" )
# # Open Youtub
        elif "open youtube" in query:
            chrome_path = "C:\\Users\\rsach\\OneDrive\\Documents\\OneDrive\\Desktop\\YouTube.lnk"  # Update with correct path
            os.startfile(chrome_path)
# # close youtub
        elif "close youtub" in query:
            speak("ok sir, closing youtub")
            os.system("taskkill /f /im chrome_proxy.exe" )




# # Open command prompt
        elif "open command prompt" in query:
            os.system("start cmd")
# # close command prompt
        elif "close command prompt" in query:
            os.system("taskkill /f /im cmd.exe")

# # open Camera
        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break;
            cap.release()
            cv2.destroyAllWindows()

        elif "close camera" in query:
            cap.release()
            cv2.destroyAllWindows()
            speak("Camera closed successfully.")


        ## Play Music
        elif "play music" in query:
            music_dir = "D:\\Downloads\\music"
            songs = os.listdir(music_dir)
            rd = random.choice(songs)
            os.startfile(os.path.join(music_dir, rd))
        elif "stop music" in query:
            speak("ok sir")
            os.system("taskkill /f /im Music.exe")

## IP Address
        elif "ip address" in query:
            ip = get('https://api.ipify.org/').text
            speak(f"your IP address is {ip}")


## Wikipedia
        elif "what is " in query or "search on wikipedia" in query:
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
        elif "tell me a joke" in query or "tell me one more joke" in query:
            joke = pyjokes.get_joke(language='en', category='neutral')
            speak(joke)

        elif "no thanks" in query or "stop" in query:
            speak("thanks for using me sir , have a good day.")
            sys.exit()


        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.keyDown("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        # speak("sir, do you have any other work")



