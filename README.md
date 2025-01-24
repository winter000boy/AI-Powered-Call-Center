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
   git clone https://github.com/winter000boy/AI-Powered-Call-Center.git
   cd AI-Powered-Call-Center



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
      <ul>
            <li>Click "Start Call" to begin interaction</li>
            <li>Use the "Speak" button for voice input</li>
            <li>Click "End Call" to finish the session</li>
      </ul>

3. Train Information
The system includes information for:
   <ul>
   <li>Rajdhani Express (12345)</li>
   <li>Shatabdi Express (67890)</li>
   </ul>




4. FAQ Topics
<ul>
<li>Ticket Cancellation</li>
<li>Luggage Allowance</li>
</ul>




5. Technical Details:

<ul>
    <li>Built with Streamlit for web interface</li>
    <li>Uses Google Gemini 1.5 Pro for AI responses</li>
    <li>Implements pyttsx3 for text-to-speech</li>
    <li>Uses speech_recognition for voice input</li>
    <li>Maintains conversation history in session state</li>
</ul>

<h2>Contributing</h2>
<p>Contributions are welcome! Please feel free to submit a Pull Request.</p>
