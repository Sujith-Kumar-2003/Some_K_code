import streamlit as st

def render_chat_history():
    """Loops through the session state and draws all past messages."""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])