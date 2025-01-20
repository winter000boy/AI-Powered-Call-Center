import os
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import requests
import json
from langchain.agents import initialize_agent, Tool
from langchain.chat_models import ChatOpenAI
from langchain_core.language_models import BaseLLM

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv('GEMINI_API_KEY')  # Use your Gemini API key
csv_file = "railway_data.csv"  # Path to your CSV file
railway_data = pd.read_csv(csv_file)

# Initialize pyttsx3 for text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

# Function to convert text to speech
def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to speech and convert to text
def listen_to_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your query...")
        text_to_speech("Hello Sir, I’m speaking from Indian Railways. How may I assist you?")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            print(f"User Query: {query}")
            return query
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError:
            print("Sorry, I couldn't request results; check your internet connection.")
            return None

# Function to query the Gemini API
def query_gemini_api(query):
    url = "https://generativelanguage.googleapis.com/v1beta2/models/gemini-1.5:generateText"
    headers = {"Authorization": f"Bearer {gemini_api_key}", "Content-Type": "application/json"}
    payload = {"prompt": {"text": query}}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json().get('candidates', [{}])[0].get('output', "No valid response from Gemini.")
    else:
        return "Sorry, I couldn't get a response from the Gemini API."

# Function to query the database for PNR and train details
def query_database(pnr_number):
    result = railway_data[railway_data['PNR'] == int(pnr_number)]
    if not result.empty:
        train_name = result.iloc[0]['Train Name']
        status = result.iloc[0]['Status']
        return f"PNR {pnr_number} is for train '{train_name}'. Current status is: {status}."
    else:
        return f"No details found for PNR {pnr_number}."

# Initialize LangChain model and agent
tools = [
    Tool(name="Gemini API Query", func=query_gemini_api, description="Fetch information using Gemini AI."),
    Tool(name="Database Query", func=query_database, description="Query railway database for PNR or train details.")
]

llm = ChatOpenAI(temperature=0)  # Replace with a Gemini-based implementation if necessary
agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description", verbose=True)

# Function to handle queries with LangChain
def handle_query(query):
    response = agent.run(query)
    return response

# Streamlit UI
st.set_page_config(page_title="AI Powered Call Center", layout="wide")
st.title("AI Powered Call Center")

# Call Simulation: Start the call and process voice input
if st.button("Start Call"):
    st.write("**Agent Raj is now attending the call. Please speak your query.**")
    with st.spinner("Agent Raj is listening..."):
        query = listen_to_audio()  # Process voice input
        if query:
            st.write("User's Query:", query)
            response = handle_query(query)  # Process query
            st.write("Agent Raj's Response:", response)

            # Convert response to speech
            text_to_speech(response)
        else:
            st.error("No query received or could not understand the query.")

# Text input for user query (optional)
query = st.text_input("Enter your query (e.g., 'What is the status of my PNR 123456?')")

# Button to submit query (text input)
if st.button("Submit Query"):
    if query:
        with st.spinner("Processing..."):
            response = handle_query(query)
            st.success("Query processed successfully!")
            st.write("Response Text:", response)
            text_to_speech(response)
    else:
        st.error("Please enter a query.")

# Button to simulate the end of the call
if st.button("End Call"):
    st.write("Thank you for calling Indian Railways! Goodbye.")
    st.balloons()

# Footer with contact details
st.markdown("---")
st.markdown("**Contact Support:** support.IndianRailway@gmail.com")
