import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
from streamlit_chat import message
import speech_recognition as sr
import pyttsx3
import json

# Railway Database
RAILWAY_DATA = {
    "train_schedules": {
        "12345": {
            "train_name": "Rajdhani Express",
            "departure_time": "10:00 AM",
            "arrival_time": "8:00 PM",
            "days_of_operation": ["Monday", "Wednesday", "Friday"]
        },
        "67890": {
            "train_name": "Shatabdi Express",
            "departure_time": "6:00 AM",
            "arrival_time": "2:00 PM",
            "days_of_operation": ["Daily"]
        }
    },
    "faqs": {
        "ticket_cancellation": "Tickets can be cancelled up to 4 hours before the train's departure.",
        "luggage_allowance": "Passengers are allowed to carry 40kg in sleeper class and 50kg in AC classes."
    }
}

# Helper functions for train and FAQ information
def get_train_info(train_number):
    return RAILWAY_DATA["train_schedules"].get(train_number, None)

def get_faq_info(topic):
    return RAILWAY_DATA["faqs"].get(topic.lower(), None)

# Load environment variables
load_dotenv()

# Configure Generative AI API
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

# Initialize Generative AI model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
)

# Create system prompt
SYSTEM_PROMPT = f"""
You are Raj, a professional call center employee at Indian Railways.
Use the following railway information to assist customers:

Train Schedules:
{json.dumps(RAILWAY_DATA['train_schedules'], indent=2)}

FAQs:
{json.dumps(RAILWAY_DATA['faqs'], indent=2)}

When answering:
1. If asked about train schedules, look up the train number in the database
2. For general questions, check the FAQs first
3. Always maintain a professional tone
4. Start with: "Hello, this is Raj from Indian Railways."
5. End with: "Is there anything else I can help you with?"
"""

chat_session = model.start_chat(history=[])
chat_session.send_message(SYSTEM_PROMPT)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

def speak_text(text):
    """Convert text to speech."""
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Error in text-to-speech: {str(e)}")

def recognize_speech():
    """Convert speech to text."""
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = recognizer.listen(source, timeout=5)
            return recognizer.recognize_google(audio)
    except sr.RequestError:
        st.error("Could not request results; check your internet connection")
        return None
    except sr.UnknownValueError:
        st.warning("Could not understand audio")
        return None
    except Exception as e:
        st.error(f"Error in speech recognition: {str(e)}")
        return None

def run_chat(user_input):
    """Enhanced chat function with data lookup."""
    try:
        # Check if query contains train number
        train_numbers = [num for num in RAILWAY_DATA["train_schedules"].keys() if num in user_input]
        if train_numbers:
            train_info = get_train_info(train_numbers[0])
            context = f"Train Information: {json.dumps(train_info)}\n"
            user_input = context + user_input

        # Check for FAQ keywords
        for topic in RAILWAY_DATA["faqs"].keys():
            if topic in user_input.lower():
                faq_info = get_faq_info(topic)
                context = f"FAQ Information: {faq_info}\n"
                user_input = context + user_input

        response = chat_session.send_message(user_input)
        return response.text
    except Exception as e:
        st.error(f"Error in chat processing: {str(e)}")
        return "I'm sorry, I couldn't process that request."

# Streamlit UI
st.title("🚂 Indian Railways Customer Service")
st.subheader("24/7 Virtual Call Center")

# Call status
if 'call_active' not in st.session_state:
    st.session_state.call_active = False
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Custom CSS for round buttons
st.markdown(
    """
    <style>
    .round-button {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: none;
        color: white;
        font-size: 16px;
        cursor: pointer;
    }
    .call-button {
        background-color: green;
    }
    .end-call-button {
        background-color: red;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Call controls
col1, col2 = st.columns(2)
with col1:
    if st.button("📞 Start Call", key="start_call", disabled=st.session_state.call_active, 
                 use_container_width=True):
        st.session_state.call_active = True
        welcome_msg = "Hello, this is Raj from Indian Railways. How may I assist you today?"
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
        speak_text(welcome_msg)

with col2:
    if st.button("🔚 End Call", key="end_call", disabled=not st.session_state.call_active, 
                 use_container_width=True):
        st.session_state.call_active = False
        goodbye_msg = "Thank you for calling Indian Railways. Have a great day!"
        st.session_state.messages.append({"role": "assistant", "content": goodbye_msg})
        speak_text(goodbye_msg)
        st.session_state.messages = []

# Show conversation interface only when call is active
if st.session_state.call_active:
    st.write("---")
    st.write("📱 Call in progress...")

    if st.button("🎤 Speak"):
        user_input = recognize_speech()
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.spinner("Processing..."):
                response = run_chat(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
                speak_text(response)

# Display conversation history
for msg in st.session_state.messages:
    message(msg["content"], is_user=(msg["role"] == "user"))

# Footer
st.markdown("---")
st.markdown("**Emergency Contact:** 139 | **Customer Care:** 1800-111-139")
