import streamlit as st
import uuid

from utils.ui_constants import GREETING_MESSAGE

def get_session_id():
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    return st.session_state["session_id"]

def print_message(message, role, save=True):
    """Print a message with a role"""    
    with st.chat_message(role):
        st.markdown(message, unsafe_allow_html=True)
    if save:
        st.session_state.messages.append({"content": message, "role": role})

def save_message(message, role):
    """Save a message to the session state"""
    st.session_state.messages.append({"content": message, "role": role})

def print_messages():
    """Print all messages in the session state"""
    for message in st.session_state.messages:
        print_message(message["content"], message["role"], save=False)

def print_greeting_message():
    """Print the greeting message"""
    if "greeting_shown" not in st.session_state:
        st.session_state.greeting_shown = False
    
    if not st.session_state.greeting_shown:
        st.session_state.greeting_shown = True
        save_message(GREETING_MESSAGE, "assistant")