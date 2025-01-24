# AI-Powered Railway Call Center

## Overview
An interactive virtual call center application for Indian Railways using Streamlit, Google's Gemini AI, and speech recognition capabilities. The system provides real-time train information, handles customer queries, and supports voice interactions.

## Features
- 🎙️ Voice Recognition: Supports speech-to-text for natural conversations
- 🔊 Text-to-Speech: Provides spoken responses for accessibility
- 🤖 AI-Powered Responses: Uses Google Gemini for intelligent conversations
- 🚂 Real-time Train Information: Access to train schedules and status
- ❓ FAQ System: Quick answers to common railway queries
- 💻 Interactive UI: Clean and responsive Streamlit interface

## Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Internet connection for speech recognition
- Microphone for voice input

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd railway-call-center


2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate  # Windows


3. Install dependencies:
   ```bash
   pip install -r requirements.txt


4. Create a .env file and add your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_api_key_here


5. Usage
   
1. Start the application:
   ```bash
   streamlit run app.py


2. Use the interface:
      <ol>
            <li>Click "Start Call" to begin interaction</li>
            <li>Use the "Speak" button for voice input</li>
            <li>Click "End Call" to finish the session</li>
      </ol>

Train Information
The system includes information for:

Rajdhani Express (12345)
Shatabdi Express (67890)


FAQ Topics
Ticket Cancellation
Luggage Allowance


Emergency Contacts
Railway Emergency: 139
Customer Care: 1800-111-139


Technical Details:

Built with Streamlit for web interface
Uses Google Gemini 1.5 Pro for AI responses
Implements pyttsx3 for text-to-speech
Uses speech_recognition for voice input
Maintains conversation history in session state
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
#### MIT License