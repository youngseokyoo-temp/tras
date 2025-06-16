import streamlit as st
from app.utils.ui_constants import PROJECT_TITLE, PROJECT_ICON, PROJECT_LOGO_HTML, CHAT_INPUT_PLACEHOLDER

# Page Config
st.set_page_config(
    page_title=PROJECT_TITLE,
    page_icon=PROJECT_ICON,
)
st.markdown(PROJECT_LOGO_HTML, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("모델 설정")

    model_provider = st.selectbox(
        "모델 제공자",
        ["ChatGPT", "Anthropic", "Gemini"],
        index=0
    )
    

# Chat
chat_input = st.chat_input(CHAT_INPUT_PLACEHOLDER)
if chat_input:
    st.chat_message("user").write(chat_input)
    st.chat_message("assistant").write(chat_input)