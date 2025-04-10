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
import traceback
import tkinter as tk
from assistant_ui import VirtualAssistantUI
import threading
from dotenv import load_dotenv
import requests

load_dotenv()

class VirtualAssistant:
    def __init__(self, ui=None):
        self.ui = ui
        self.is_running = False
        self.engine = pyttsx3.init("sapi5")
        self.voices = self.engine.getProperty("voices")
        self.engine.setProperty("voice", self.voices[1].id)
        self.engine.setProperty("rate", 140)

    def speak(self, audio):
        try:
            self.engine.say(audio)
            if self.ui:
                self.ui.update_output(audio)
            print(audio)
            self.engine.runAndWait()
        except Exception as e:
            print("Error in speak function:")
            traceback.print_exc()

    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.update_ui("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, timeout=10, phrase_time_limit=10)

        try:
            self.update_ui("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            self.update_ui(f"User said: {query}")
            return query.lower()
        except Exception as e:
            self.speak("Listening....")
            return "None"

    def update_ui(self, message):
        if self.ui:
            self.ui.update_output(message)
        print(message)

    def greet(self):
        hour = datetime.datetime.now().hour
        current_time = datetime.datetime.now().strftime("%I:%M %p")

        if 0 <= hour < 12:
            self.speak("Good morning!")
        elif 12 <= hour < 18:
            self.speak("Good afternoon!")
        else:
            self.speak("Good evening!")

        self.speak(f"It is {current_time}")
        self.speak("Hello sir. How can I help you?")

    def sendEmail(self, to, content):
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            email = os.getenv('EMAIL')
            password = os.getenv('EMAIL_PASSWORD')
            server.login(email, password)
            server.sendmail(email, to, content)
            server.close()
            self.speak("Email has been sent successfully!")
        except Exception as e:
            print(e)
            self.speak("Sorry, I was unable to send the email.")

    def process_commands(self, query):
        try:
            # Conversation commands
            if "hello" in query:
                self.speak("Hello sir, how are you?")
            elif "fine" in query or "good" in query:
                self.speak("That's great to hear, sir")
            elif "how are you" in query:
                self.speak("I'm doing well, thank you for asking")
            elif "what is your name" in query:
                self.speak("My name is Nova, I am your virtual assistant")
            elif "thank you" in query or "thanks" in query:
                self.speak("You're welcome, sir")

            # System commands
            elif "open notepad" in query:
                self.speak("Opening Notepad")
                os.startfile("C:\\Windows\\System32\\notepad.exe")
            elif "close notepad" in query:
                self.speak("Closing Notepad")
                os.system("taskkill /f /im notepad.exe")
            elif "open command prompt" in query or "open cmd" in query:
                self.speak("Opening Command Prompt")
                os.system("start cmd")
            elif "open calculator" in query:
                self.speak("Opening Calculator")
                os.startfile("C:\\Windows\\System32\\calc.exe")
            elif "take screenshot" in query:
                self.speak("Taking screenshot")
                img = pyautogui.screenshot()
                img.save(f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                self.speak("Screenshot saved")

            # Media controls
            elif "volume up" in query:
                pyautogui.press("volumeup", presses=5)
                self.speak("Volume increased")
            elif "volume down" in query:
                pyautogui.press("volumedown", presses=5)
                self.speak("Volume decreased")
            elif "mute" in query:
                pyautogui.press("volumemute")
                self.speak("Audio muted")

            # Application controls
            elif "minimize window" in query:
                pyautogui.hotkey('win', 'down')
                self.speak("Window minimized")
            elif "maximize window" in query:
                pyautogui.hotkey('win', 'up')
                self.speak("Window maximized")
            elif "switch window" in query:
                pyautogui.hotkey('alt', 'tab')
                self.speak("Switching window")
            elif "close window" in query:
                pyautogui.hotkey('alt', 'f4')
                self.speak("Window closed")

            # System tools
            elif "task manager" in query:
                pyautogui.hotkey('ctrl', 'shift', 'esc')
                self.speak("Opening Task Manager")
            elif "settings" in query:
                os.system('start ms-settings:')
                self.speak("Opening Settings")
            elif "control panel" in query:
                os.system('control panel')
                self.speak("Opening Control Panel")

            # File operations
            elif "create folder" in query:
                self.speak("What should I name the folder?")
                folder_name = self.take_command().lower()
                if folder_name != "none":
                    os.makedirs(folder_name, exist_ok=True)
                    self.speak(f"Created folder named {folder_name}")
            elif "delete folder" in query:
                self.speak("Which folder should I delete?")
                folder_name = self.take_command().lower()
                if folder_name != "none" and os.path.exists(folder_name):
                    os.rmdir(folder_name)
                    self.speak(f"Deleted folder {folder_name}")

            # Web commands
            elif "open youtube" in query:
                self.speak("Opening YouTube")
                webbrowser.open("https://youtube.com")
            elif "search youtube" in query:
                self.speak("What should I search on YouTube?")
                search_term = self.take_command().lower()
                if search_term != "none":
                    kit.playonyt(search_term)
            elif "open google" in query:
                self.speak("What should I search on Google?")
                search_term = self.take_command().lower()
                if search_term != "none":
                    webbrowser.open(f"https://google.com/search?q={search_term}")
            elif "wikipedia" in query:
                self.speak("What should I search on Wikipedia?")
                search_term = self.take_command().lower()
                if search_term != "none":
                    try:
                        results = wikipedia.summary(search_term, sentences=2)
                        self.speak(f"According to Wikipedia: {results}")
                    except:
                        self.speak("Sorry, I couldn't find that on Wikipedia")

            # Quick searches
            elif "define" in query:
                search_term = query.replace("define", "").strip()
                webbrowser.open(f"https://www.dictionary.com/browse/{search_term}")
                self.speak(f"Looking up definition of {search_term}")
            elif "translate" in query:
                text = query.replace("translate", "").strip()
                webbrowser.open(f"https://translate.google.com/?text={text}")
                self.speak(f"Translating: {text}")

            # Email and communication
            elif "send email" in query:
                try:
                    self.speak("What should I say in the email?")
                    content = self.take_command().lower()
                    self.speak("Who should I send this to?")
                    to = self.take_command().lower()
                    if content != "none" and to != "none":
                        self.sendEmail(to, content)
                except Exception as e:
                    self.speak("Sorry, I couldn't send the email")

            # Time and date
            elif "time" in query:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                self.speak(f"The current time is {current_time}")
            elif "date" in query:
                current_date = datetime.datetime.now().strftime("%B %d, %Y")
                self.speak(f"Today's date is {current_date}")

            # System information
            elif "ip address" in query:
                ip = get('https://api.ipify.org').text
                self.speak(f"Your IP address is {ip}")
            elif "cpu usage" in query:
                import psutil
                cpu = psutil.cpu_percent()
                self.speak(f"CPU is at {cpu} percent")
            elif "battery" in query:
                import psutil
                battery = psutil.sensors_battery()
                self.speak(f"Battery is at {battery.percent} percent")
            elif "memory usage" in query:
                import psutil
                memory = psutil.virtual_memory()
                self.speak(f"Memory usage is {memory.percent}%")
            elif "disk space" in query:
                import psutil
                disk = psutil.disk_usage('/')
                free_gb = round(disk.free / (1024**3), 2)
                self.speak(f"You have {free_gb} GB of free disk space")

            # Entertainment
            elif "tell me a joke" in query:
                joke = pyjokes.get_joke()
                self.speak(joke)
            elif "play music" in query:
                music_dir = "C:\\Users\\YourUsername\\Music"  # Change this to your music directory
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, random.choice(songs)))

            # Weather (requires WeatherAPI key)
            elif "weather" in query:
                try:
                    self.speak("Which city's weather would you like to know?")
                    city = self.take_command().lower()
                    if city != "none":
                        api_key = os.getenv('WEATHER_API_KEY')
                        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
                        
                        response = requests.get(url)
                        if response.status_code == 200:
                            weather_data = response.json()
                            location = weather_data['location']
                            current = weather_data['current']
                            
                            # Extract weather information
                            city_name = location['name']
                            region = location['region']
                            country = location['country']
                            temp_c = current['temp_c']
                            feels_like = current['feelslike_c']
                            humidity = current['humidity']
                            condition = current['condition']['text']
                            # wind_speed = current['wind_kph']
                            
                            weather_info = (
                                f"The current weather in {city_name} is:\n"
                                f"Temperature: {temp_c}°C\n"
                                f"Feels like: {feels_like}°C\n"
                                f"Humidity: {humidity}%\n"
                                # f"Wind Speed: {wind_speed} km/h\n"
                                f"Conditions: {condition}"
                            )
                            
                            self.speak(weather_info)
                        else:
                            self.speak(f"Sorry, I couldn't find weather information for {city}")
                except Exception as e:
                    print(f"Weather Error: {str(e)}")
                    self.speak("Sorry, I encountered an error getting the weather information")

            # Clipboard operations
            elif "copy" in query:
                pyautogui.hotkey('ctrl', 'c')
                self.speak("Content copied")
            elif "paste" in query:
                pyautogui.hotkey('ctrl', 'v')
                self.speak("Content pasted")
            elif "cut" in query:
                pyautogui.hotkey('ctrl', 'x')
                self.speak("Content cut")

            # Timer and reminders
            elif "set timer" in query:
                self.speak("How many minutes?")
                try:
                    minutes = int(self.take_command())
                    self.speak(f"Timer set for {minutes} minutes")
                    threading.Timer(minutes * 60, lambda: self.speak("Timer finished!")).start()
                except ValueError:
                    self.speak("Sorry, I couldn't understand the time")

            # System control
            elif "shutdown" in query:
                self.speak("Are you sure you want to shutdown the computer?")
                if "yes" in self.take_command().lower():
                    os.system("shutdown /s /t 1")
            elif "restart" in query:
                self.speak("Are you sure you want to restart the computer?")
                if "yes" in self.take_command().lower():
                    os.system("shutdown /r /t 1")

            # Exit commands
            elif "stop" in query or "exit" in query or "goodbye" in query:
                self.speak("Thanks for using me sir, have a good day.")
                self.stop()

        except Exception as e:
            self.speak("Sorry, I encountered an error while processing your command")
            print(f"Error: {str(e)}")

    def run(self):
        self.is_running = True
        self.greet()
        while self.is_running:
            query = self.take_command()
            if query != "None":
                self.process_commands(query)

    def stop(self):
        self.is_running = False

def main():
    root = tk.Tk()
    ui = VirtualAssistantUI(root)
    assistant = VirtualAssistant(ui)
    ui.set_assistant(assistant)
    root.mainloop()

if __name__ == "__main__":
    main()



