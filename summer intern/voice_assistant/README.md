# Advanced Voice Assistant

A comprehensive voice assistant with natural language processing, task automation, and smart home integration capabilities.

## Features

### Core Functionality
- **Speech Recognition**: Convert voice commands to text using Google's Speech Recognition API
- **Text-to-Speech**: Respond to users with synthesized voice output
- **Natural Language Processing**: Understand and interpret user queries
- **Task Automation**: Perform various tasks automatically

### Built-in Capabilities
- **Weather Information**: Get real-time weather updates for any city
- **Email Integration**: Send emails via voice commands
- **Reminder Management**: Set, view, and manage reminders
- **General Knowledge**: Answer questions using Wikipedia API
- **Custom Commands**: Create personalized voice commands
- **Smart Home Ready**: Framework for integrating IoT devices

### Security & Privacy Features
- **Configuration File**: Secure storage of API keys and credentials
- **Custom Commands Storage**: User-defined commands saved locally
- **Error Handling**: Comprehensive error management for all operations
- **Privacy Protection**: All data stored locally unless explicitly shared

## Requirements

```bash
pip install SpeechRecognition pyttsx3 requests
```

### Python Version
- Python 3.7 or higher

## Installation

1. Clone the repository
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your credentials (see Configuration section)
4. Run the assistant:
   ```bash
   python main.py
   ```

## Configuration

### Setting Up API Keys and Credentials

Create/edit `assistant_config.json`:

```json
{
    "weather_api_key": "YOUR_OPENWEATHER_API_KEY",
    "email": "your_email@gmail.com",
    "email_password": "your_app_password",
    "reminders": []
}
```

### Weather API Setup
1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Add it to `assistant_config.json`

### Email Setup (Gmail)
1. Enable 2-Factor Authentication on your Gmail account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the generated password in your configuration file
4. **Never use your actual Gmail password**

## Available Commands

### Weather
```
"weather in [city]"
"what's the weather like in London?"
```

### Email
```
"send email"
```
Follow the prompts to provide recipient, subject, and message.

### Reminders
```
"set reminder [reminder text]"
"show reminders"
"my reminders"
```

### Knowledge Questions
```
"who is Albert Einstein?"
"what is photosynthesis?"
"tell me about machine learning"
```

### Custom Commands
```
"add command"
```
Create custom voice commands with personalized responses.

### General
```
"help" - Show available commands
"who are you" - About the assistant
"hello" or "hi" - Greeting
"exit" or "quit" - Close the assistant
```

## File Structure

```
voice_assistant/
├── main.py                    # Main assistant application
├── README.md                  # This file
├── assistant_config.json      # Configuration file (auto-generated)
├── custom_commands.json       # Custom commands (auto-generated)
└── requirements.txt           # Python dependencies
```

## How It Works

1. **Voice Capture**: The assistant listens for voice commands using the microphone
2. **Speech-to-Text**: Converts audio to text using Google's API
3. **Command Processing**: Analyzes and identifies the requested action
4. **Task Execution**: Performs the appropriate action (fetch weather, send email, etc.)
5. **Response Generation**: Provides feedback via text-to-speech

## Error Handling

The assistant handles various error conditions:
- **Network Issues**: Gracefully handles API timeouts and failures
- **Voice Recognition Errors**: Prompts user to repeat if speech is unclear
- **Invalid Commands**: Provides helpful feedback for unrecognized commands
- **Configuration Errors**: Alerts user to missing or invalid settings

## Customization

### Adding Custom Commands

You can add custom commands through the voice interface:

```
User: "add command"
Assistant: "What is the command name?"
User: "remind me to exercise"
Assistant: "What should the assistant say?"
User: "Go for a 30-minute run or do some yoga"
```

Or manually edit `custom_commands.json`:

```json
{
    "check my schedule": "Your schedule is available in your calendar app"
}
```

### Extending Functionality

You can extend the assistant by:
1. Adding new methods to the `VoiceAssistant` class
2. Integrating with additional APIs (IFTTT, Home Assistant, etc.)
3. Adding smart home device control
4. Implementing calendar integration
5. Adding music player controls

## Privacy & Security Notes

- **Local Storage**: All personal data is stored locally on your machine
- **API Keys**: Keep your API keys confidential and never commit them to version control
- **Email Security**: Use App Passwords, not your actual Gmail password
- **Data Minimization**: Only provide necessary information to APIs
- **No Cloud Storage**: By default, no data is sent to external services except for API calls

## Limitations

- Requires active microphone input
- Speech recognition works best in quiet environments
- API services depend on internet connectivity
- Weather requires valid city names
- Gmail integration requires App Passwords (not regular passwords)

## Troubleshooting

### Microphone Not Working
- Check if your microphone is properly connected
- Verify microphone permissions in system settings
- Test with: `python -c "import speech_recognition as sr; print(sr.Microphone().list_microphone_indexes())"`

### Weather API Error
- Verify your OpenWeatherMap API key is valid
- Check internet connection
- Ensure city name is spelled correctly

### Email Not Sending
- Verify email configuration in `assistant_config.json`
- Ensure Gmail 2FA is enabled and App Password is used
- Check internet connection

### Speech Recognition Issues
- Reduce background noise
- Speak clearly and at a normal pace
- Check microphone volume levels

## Future Enhancements

- Smart home device control (Philips Hue, smart thermostats)
- Calendar and appointment management
- Music streaming integration
- Real-time translation
- Multi-language support
- Machine learning for personalized responses
- Database for storing user preferences

## Author

Created as part of Oasis Infobyte internship program

## License

This project is open source and available for educational purposes.

## Support

For issues, feature requests, or contributions, please refer to the project repository.
