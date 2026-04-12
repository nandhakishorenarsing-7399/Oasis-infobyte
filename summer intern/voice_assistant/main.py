import speech_recognition as sr
import pyttsx3
import requests
import smtplib
import json
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

class VoiceAssistant:
    def __init__(self):
        """Initialize the voice assistant with speech recognition and text-to-speech."""
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        
        # Configuration file for sensitive data
        self.config_file = 'assistant_config.json'
        self.load_config()
        
        # Custom commands dictionary
        self.custom_commands = {}
        self.load_custom_commands()
        
        print("Voice Assistant initialized. Say 'hello' to get started.")
        self.speak("Voice Assistant ready. How can I help you?")
    
    def speak(self, text):
        """Convert text to speech."""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
    
    def listen(self, timeout=10):
        """Listen to user voice input and convert to text."""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout)
            
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        
        except sr.UnknownValueError:
            response = "Sorry, I didn't understand that. Could you please repeat?"
            self.speak(response)
            return None
        
        except sr.RequestError:
            response = "Sorry, there's an issue with the speech recognition service."
            self.speak(response)
            return None
        
        except sr.Timeout:
            response = "I didn't hear anything. Please try again."
            self.speak(response)
            return None
    
    def load_config(self):
        """Load configuration from JSON file for APIs and sensitive data."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                "weather_api_key": "YOUR_OPENWEATHER_API_KEY",
                "email": "your_email@gmail.com",
                "email_password": "your_app_password",
                "reminders": []
            }
            self.save_config()
    
    def save_config(self):
        """Save current configuration to JSON file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def load_custom_commands(self):
        """Load user-defined custom commands."""
        commands_file = 'custom_commands.json'
        if os.path.exists(commands_file):
            with open(commands_file, 'r') as f:
                self.custom_commands = json.load(f)
    
    def save_custom_commands(self):
        """Save custom commands to file."""
        with open('custom_commands.json', 'w') as f:
            json.dump(self.custom_commands, f, indent=4)
    
    def get_weather(self, city):
        """Fetch weather information for a given city."""
        try:
            api_key = self.config.get('weather_api_key')
            if api_key == "YOUR_OPENWEATHER_API_KEY":
                response = "Please configure your weather API key in the assistant_config.json file."
                self.speak(response)
                return response
            
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                weather_description = data['weather'][0]['description']
                temperature = data['main']['temp']
                result = f"The weather in {city} is {weather_description} with a temperature of {temperature} degrees Celsius."
                self.speak(result)
                return result
            else:
                error_msg = "I couldn't find weather information for that location."
                self.speak(error_msg)
                return error_msg
        
        except requests.exceptions.Timeout:
            error_msg = "The weather service is taking too long to respond."
            self.speak(error_msg)
            return error_msg
        
        except Exception as e:
            error_msg = f"Error fetching weather: {str(e)}"
            print(error_msg)
            self.speak("Sorry, I couldn't fetch the weather information.")
            return error_msg
    
    def send_email(self, recipient, subject, body):
        """Send an email."""
        try:
            sender_email = self.config.get('email')
            email_password = self.config.get('email_password')
            
            if sender_email == "your_email@gmail.com":
                response = "Please configure your email settings in assistant_config.json"
                self.speak(response)
                return response
            
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = recipient
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))
            
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender_email, email_password)
            server.send_message(message)
            server.quit()
            
            response = f"Email sent successfully to {recipient}."
            self.speak(response)
            return response
        
        except smtplib.SMTPAuthenticationError:
            error_msg = "Email authentication failed. Please check your credentials."
            self.speak(error_msg)
            return error_msg
        
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            print(error_msg)
            self.speak("Sorry, I couldn't send the email.")
            return error_msg
    
    def set_reminder(self, reminder_text):
        """Set a reminder."""
        try:
            reminder = {
                "text": reminder_text,
                "time": datetime.now().isoformat()
            }
            self.config['reminders'].append(reminder)
            self.save_config()
            
            response = f"Reminder set: {reminder_text}"
            self.speak(response)
            return response
        
        except Exception as e:
            error_msg = f"Error setting reminder: {str(e)}"
            print(error_msg)
            self.speak("Sorry, I couldn't set the reminder.")
            return error_msg
    
    def get_reminders(self):
        """Get all reminders."""
        reminders = self.config.get('reminders', [])
        if reminders:
            response = f"You have {len(reminders)} reminders."
            self.speak(response)
            for reminder in reminders:
                print(f"- {reminder['text']}")
            return response
        else:
            response = "You have no reminders set."
            self.speak(response)
            return response
    
    def answer_question(self, question):
        """Answer general knowledge questions using Wikipedia API."""
        try:
            url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "titles": question,
                "prop": "extracts",
                "explaintext": True,
                "exintro": True
            }
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            
            pages = data["query"]["pages"]
            page_id = next(iter(pages))
            page = pages[page_id]
            
            if "extract" in page:
                extract = page["extract"][:200]  # Limit response length
                self.speak(extract)
                return extract
            else:
                error_msg = "I couldn't find information about that topic."
                self.speak(error_msg)
                return error_msg
        
        except Exception as e:
            error_msg = f"Error answering question: {str(e)}"
            print(error_msg)
            self.speak("Sorry, I couldn't find an answer to that question.")
            return error_msg
    
    def add_custom_command(self, command_name, response):
        """Add a custom command."""
        try:
            self.custom_commands[command_name.lower()] = response
            self.save_custom_commands()
            result = f"Custom command '{command_name}' added successfully."
            self.speak(result)
            return result
        
        except Exception as e:
            error_msg = f"Error adding custom command: {str(e)}"
            print(error_msg)
            self.speak("Sorry, I couldn't add the custom command.")
            return error_msg
    
    def execute_custom_command(self, command_name):
        """Execute a custom command."""
        if command_name in self.custom_commands:
            response = self.custom_commands[command_name]
            self.speak(response)
            return response
        else:
            error_msg = "Custom command not found."
            self.speak(error_msg)
            return error_msg
    
    def process_command(self, command):
        """Process and execute commands based on user input."""
        if not command:
            return
        
        # Check custom commands first
        if command in self.custom_commands:
            return self.execute_custom_command(command)
        
        # Built-in commands
        if 'weather' in command:
            try:
                city = command.split('weather in')[-1].strip()
                if city:
                    return self.get_weather(city)
            except:
                self.speak("Please specify a city for weather information.")
        
        elif 'send email' in command:
            self.speak("Who should I send the email to?")
            recipient = self.listen()
            if recipient:
                self.speak("What is the subject?")
                subject = self.listen()
                if subject:
                    self.speak("What is the message?")
                    body = self.listen()
                    if body:
                        return self.send_email(recipient, subject, body)
        
        elif 'set reminder' in command:
            self.speak("What should I remind you about?")
            reminder_text = self.listen()
            if reminder_text:
                return self.set_reminder(reminder_text)
        
        elif 'show reminders' in command or 'my reminders' in command:
            return self.get_reminders()
        
        elif 'add command' in command:
            self.speak("What is the command name?")
            cmd_name = self.listen()
            if cmd_name:
                self.speak("What should the assistant say?")
                response = self.listen()
                if response:
                    return self.add_custom_command(cmd_name, response)
        
        elif 'help' in command:
            help_text = """
            Available commands:
            - 'weather in [city]' - Get weather information
            - 'send email' - Send an email
            - 'set reminder' - Set a reminder
            - 'show reminders' - View all reminders
            - 'add command' - Add a custom command
            - 'who are you' - About this assistant
            - 'exit' or 'quit' - Close the assistant
            - Ask any question for general knowledge
            """
            self.speak("Here are my available commands. Check the console for details.")
            print(help_text)
        
        elif 'who are you' in command:
            about = "I'm your advanced voice assistant with natural language processing capabilities. I can help with weather, emails, reminders, and much more."
            self.speak(about)
        
        elif 'hello' in command or 'hi' in command:
            response = "Hello! How can I assist you today?"
            self.speak(response)
        
        else:
            # Try to answer as a general knowledge question
            return self.answer_question(command)
    
    def run(self):
        """Main loop for the voice assistant."""
        print("\n=== Voice Assistant Started ===")
        print("Say 'help' for available commands")
        print("Say 'exit' to quit\n")
        
        while True:
            try:
                command = self.listen()
                
                if command:
                    if 'exit' in command or 'quit' in command:
                        self.speak("Goodbye! Have a great day.")
                        print("Voice Assistant closed.")
                        break
                    
                    self.process_command(command)
            
            except KeyboardInterrupt:
                print("\nVoice Assistant interrupted.")
                self.speak("Goodbye!")
                break
            
            except Exception as e:
                print(f"Unexpected error: {e}")
                self.speak("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()
