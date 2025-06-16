import streamlit as st

from utils.ui_constants import PROJECT_TITLE, PROJECT_ICON, PROJECT_LOGO_HTML, CHAT_INPUT_PLACEHOLDER, MODEL_LOADING_ERROR_MESSAGE
from utils.streamlit_helpers import print_message, print_messages, print_greeting_message, get_session_id, save_message
from utils.logger import get_logger
from llms import get_llm_instance, AVAILABLE_MODELS
from llms.config import get_model_versions, get_model_config

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
        list(AVAILABLE_MODELS.keys()),
        index=0
    )
    
    available_versions = get_model_versions(model_provider)
    model_version = st.selectbox(
        f"{model_provider} 버전",
        available_versions,
        index=0
    )
    
    if model_provider and model_version:
        config = get_model_config(model_provider, model_version)
        st.info(f"**선택된 모델**: {model_version}")
        
        with st.expander("고급 설정"):
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=config.temperature,
                step=0.1,
                help="응답의 창의성을 조절합니다. 높을수록 더 창의적입니다."
            )

# Get Ready for Chat
if "messages" not in st.session_state: 
    st.session_state.messages = []
session_id = get_session_id()
logger = get_logger(session_id)

# Chat  
print_greeting_message()
print_messages()
chat_input = st.chat_input(CHAT_INPUT_PLACEHOLDER)
if chat_input:
    print_message(chat_input, "user")

    llm = get_llm_instance(
        log=logger,
        provider=model_provider,
        version=model_version,
        temperature=temperature,
    )

    if not llm:
        print_message(MODEL_LOADING_ERROR_MESSAGE, "system")
        st.stop()

    # LLM Response
    with st.chat_message("assistant"):
        response = ""
        message_placeholder = st.empty()
        for chunk in llm.stream(chat_input):
            response += chunk.content
            message_placeholder.markdown(response)
        save_message(response, "assistant")