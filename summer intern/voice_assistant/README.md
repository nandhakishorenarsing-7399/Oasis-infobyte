# Jarvis Voice Assistant

A voice-controlled assistant inspired by Marvel's Jarvis, built to run in the terminal with microphone input.

## Features
- Real-time voice command recognition using the laptop microphone
- Natural voice responses using `pyttsx3`
- Local command execution:
  - Open Calculator
  - Open Notepad
  - Open Command Prompt
  - Open File Explorer
- Online actions:
  - Play YouTube videos
  - Search Google
  - Get weather updates
  - Open websites
- Conversation-style interaction with Jarvis-style responses
- Wake-word handling for a Hollywood-style assistant experience

## Requirements
- Python 3.x
- `SpeechRecognition`
- `pyttsx3`
- `pywhatkit`
- `requests`

## Setup
1. Install required libraries:
   ```bash
   pip install SpeechRecognition pyttsx3 pywhatkit requests
   ```
2. If needed, update `jarvis_config.json` with your OpenWeather API key.

## Run
```bash
cd "c:\Users\91934\OneDrive\Desktop\summer intern\voice_assistant"
python voice.py
```

## Notes
- Use a quiet environment for better voice recognition.
- Speak clearly and address the assistant as `Jarvis` for the best experience.
- Configure `jarvis_config.json` before using weather commands.
