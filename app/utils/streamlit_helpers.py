import uuid

import streamlit as st
from langgraph.checkpoint.base import Checkpoint
from langgraph.checkpoint.memory import InMemorySaver

from app.llms.factory import get_llm_instance
from app.supervisor.chatbot import get_supervisor_chatbot
from app.utils.ui_constants import (
    GREETING_MESSAGE,
    MODEL_INITIALIZING_MESSAGE,
    MODEL_LOADING_ERROR_MESSAGE,
    MODEL_SETTING_MESSAGE,
)

# Session Helpers

def get_session_id() -> str:
    """Get the session id"""
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())
    return st.session_state["session_id"]


def get_session_checkpointer() -> Checkpoint:
    """Get the session checkpointer"""
    if "checkpointer" not in st.session_state:
        st.session_state["checkpointer"] = InMemorySaver()
    return st.session_state["checkpointer"]


def get_chatbot(model_provider: str, model_version: str, temperature: float, logger):
    current_config = {
        "model_provider": model_provider,
        "model_version": model_version,
        "temperature": temperature,
    }

    if "chatbot" not in st.session_state or st.session_state.model_config != current_config:
        with st.spinner(MODEL_INITIALIZING_MESSAGE):
            llm = get_llm_instance(
                log=logger,
                provider=model_provider,
                version=model_version,
                temperature=temperature,
            )

            if not llm:
                st.error(MODEL_LOADING_ERROR_MESSAGE)
                st.stop()

            st.session_state.chatbot = get_supervisor_chatbot(llm, get_session_checkpointer())
            st.session_state.model_config = current_config

        st.success(MODEL_SETTING_MESSAGE)

    return st.session_state.chatbot

### UI Helpers


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
