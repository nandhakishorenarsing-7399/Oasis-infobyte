import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import subprocess
import requests
import json
import os
from datetime import datetime

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'jarvis_config.json')

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.95)

# Choose a more natural voice if available
voices = engine.getProperty('voices')
preferred_voice = None
for voice in voices:
    name = voice.name.lower()
    vid = voice.id.lower()
    if 'david' in name or 'david' in vid or 'zira' in name or 'zira' in vid or 'mark' in name or 'karen' in name:
        preferred_voice = voice.id
        break
if preferred_voice:
    engine.setProperty('voice', preferred_voice)

# Load or create configuration for API keys and settings
if not os.path.exists(CONFIG_FILE):
    default_config = {
        "weather_api_key": "YOUR_OPENWEATHER_API_KEY",
        "assistant_name": "jarvis"
    }
    with open(CONFIG_FILE, 'w') as file:
        json.dump(default_config, file, indent=4)

with open(CONFIG_FILE, 'r') as file:
    config = json.load(file)

ASSISTANT_NAME = config.get('assistant_name', 'jarvis').lower()

# Speak helper
def speak(text):
    message = f"{ASSISTANT_NAME.title()}: {text}"
    print(message)
    engine.say(text)
    engine.runAndWait()

# Listen helper
def listen(timeout=8, phrase_time_limit=6):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Jarvis is listening...")
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You: {command}")
        if ASSISTANT_NAME in command:
            command = command.replace(ASSISTANT_NAME, '').replace('hey', '').replace('ok', '').strip()
            if not command:
                speak('Yes, sir?')
                return listen()
        return command
    except sr.UnknownValueError:
        speak('I did not catch that, sir. Please repeat.')
        return ''
    except sr.RequestError:
        speak('Speech service is unavailable at the moment. Please check your connection.')
        return ''
    except sr.WaitTimeoutError:
        speak('I was waiting for your command but did not hear anything. Please try again.')
        return ''

# Local commands
def open_calculator():
    try:
        subprocess.Popen('calc.exe')
        speak('Launching calculator now, sir.')
    except Exception:
        speak('I am unable to open the calculator at this time.')

def open_notepad():
    try:
        subprocess.Popen('notepad.exe')
        speak('Notepad is open. Ready for your notes.')
    except Exception:
        speak('I cannot open Notepad right now.')

def open_command_prompt():
    try:
        subprocess.Popen('cmd.exe')
        speak('Command prompt is ready, sir.')
    except Exception:
        speak('I failed to open the command prompt.')

def open_explorer():
    try:
        subprocess.Popen('explorer.exe')
        speak('I have opened File Explorer for you.')
    except Exception:
        speak('File Explorer could not be opened.')

# Online and extended commands
def play_youtube(command):
    query = command.replace('play', '').replace('on youtube', '').strip()
    if not query:
        speak('What would you like me to play, sir?')
        query = listen()
    if query:
        speak(f'Playing {query} on YouTube, sir.')
        pywhatkit.playonyt(query)

def search_google(command):
    query = command.replace('search for', '').replace('search', '').strip()
    if not query:
        speak('What would you like me to search for?')
        query = listen()
    if query:
        speak(f'Searching the web for {query}, sir.')
        pywhatkit.search(query)

def get_weather(command):
    api_key = config.get('weather_api_key')
    city = command.replace('weather in', '').replace('weather', '').strip()
    if not city:
        speak('For which city, sir?')
        city = listen()
    if not city:
        return
    if api_key == 'YOUR_OPENWEATHER_API_KEY':
        speak('My weather API key is not configured. Please update jarvis_config.json.')
        return

    try:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get('cod') != 200:
            speak(f'I was unable to retrieve weather for {city}, sir.')
            return
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        speak(f'The weather in {city} is {description} with a temperature of {temp} degrees Celsius, sir.')
    except requests.RequestException:
        speak('I cannot reach the weather service right now.')

def tell_time():
    now = datetime.now().strftime('%I:%M %p')
    speak(f'The current time is {now}.')

def tell_date():
    today = datetime.now().strftime('%A, %B %d, %Y')
    speak(f'Today is {today}.')

def open_website(command):
    if 'open' in command:
        site = command.replace('open', '').strip()
        if site:
            if not site.startswith('http'):
                site = 'https://' + site
            webbrowser.open(site)
            speak(f'Opening {site}.')
        else:
            speak('Which website should I open?')
    else:
        speak('Please tell me the website to open.')

def handle_general_query(command):
    try:
        speak('Searching the web for your query.')
        pywhatkit.search(command)
    except Exception:
        speak('I could not complete the search.')

def process_command(command):
    command = command.replace(ASSISTANT_NAME, '').strip()

    if not command:
        return
    if 'open calculator' in command or 'calculator' in command:
        open_calculator()
    elif 'open notepad' in command or 'notepad' in command:
        open_notepad()
    elif 'command prompt' in command or 'cmd' in command:
        open_command_prompt()
    elif 'open explorer' in command or 'file explorer' in command or 'explorer' in command:
        open_explorer()
    elif 'play' in command and 'youtube' in command:
        play_youtube(command)
    elif 'play' in command:
        play_youtube(command)
    elif 'search for' in command or 'search' in command:
        search_google(command)
    elif 'weather' in command:
        get_weather(command)
    elif 'time' in command:
        tell_time()
    elif 'date' in command:
        tell_date()
    elif 'open ' in command and ('http' in command or '.' in command or 'website' in command):
        open_website(command)
    elif 'who are you' in command or 'what are you' in command:
        speak('I am Jarvis, your personal assistant. My mission is to make things easier for you, sir.')
    elif 'what can you do' in command or 'help' in command:
        speak('I can launch applications, search the web, play videos, provide weather updates, and manage commands in real time. Just say the word, sir.')
    elif 'how are you' in command:
        speak('I am operating at optimal capacity, sir. Ready for your next command.')
    elif 'hello' in command or 'hi' in command or 'hey' in command:
        speak('Good day, sir. Jarvis is here.')
    elif 'thank' in command or 'thanks' in command:
        speak('Always here to assist, sir.')
    elif 'exit' in command or 'quit' in command or 'stop' in command:
        speak('Shutting down now. I will be here when you need me, sir.')
        exit(0)
    else:
        speak('Understood. I am searching for an answer, sir.')
        handle_general_query(command)

if __name__ == '__main__':
    speak('Jarvis is online and ready for voice commands.')
    while True:
        command = listen()
        process_command(command)