# Voice Assistant

A simple voice assistant built with Python that listens for spoken commands, responds using text-to-speech, and performs tasks like opening applications, searching the web, playing YouTube, and checking weather.

## Features

- Speech recognition via `speech_recognition`
- Text-to-speech using `pyttsx3`
- Play YouTube videos with `pywhatkit`
- Open websites and local Windows apps
- Get current time and date
- Weather lookup using OpenWeatherMap API
- Custom assistant name and configuration via `jarvis_config.json`

## Requirements

- Python 3.8+ on Windows
- Internet connection for online commands and API requests

## Setup

1. Install dependencies:
   ```bash
   pip install SpeechRecognition pyttsx3 pywhatkit requests
   ```

2. Ensure your system has a working microphone and speakers.

3. Configure `jarvis_config.json`:
   - `weather_api_key`: Your OpenWeatherMap API key
   - `assistant_name`: Name used to trigger the assistant

   Example:
   ```json
   {
     "weather_api_key": "YOUR_OPENWEATHER_API_KEY",
     "assistant_name": "jarvis"
   }
   ```

## Usage

Run the assistant from the `voice_assistant` folder:

```bash
python voice.py
```

Speak your assistant name followed by a command, for example:

- "Jarvis open calculator"
- "Jarvis play relaxing music on YouTube"
- "Jarvis search for Python tutorials"
- "Jarvis weather in London"
- "Jarvis what is the time"

## Supported Commands

- `open calculator`
- `open notepad`
- `command prompt` / `cmd`
- `open explorer`
- `play ... youtube`
- `search for ...`
- `weather ...`
- `time`
- `date`
- `open ...` (website)
- `who are you`
- `what can you do`
- `exit` / `quit` / `stop`

## Notes

- The assistant currently uses the Google speech recognition backend.
- If the weather API key is not configured, weather requests will not work.
- This project is designed for Windows, since it opens Windows applications like `calc.exe`, `notepad.exe`, and `cmd.exe`.

## GitHub

This folder is not currently a Git repository. To add it to GitHub:

```bash
cd "c:\Users\91934\OneDrive\Desktop\summer intern\voice_assistant"
 git init
 git add .
 git commit -m "Add voice assistant README"
 git branch -M main
 git remote add origin <your-github-repo-url>
 git push -u origin main
```
