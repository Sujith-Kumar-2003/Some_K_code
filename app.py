import streamlit as st
from utils.quiz_logic import load_words, check_answer, get_hint
from utils.ui_components import render_chat_history

# 1. Setup the Page
st.set_page_config(page_title="Korean Daily Practice", page_icon="🇰🇷")
st.title("Daily Korean Practice 🇰🇷")

# 2. Initialize Session State (Memory for the app)
if "words" not in st.session_state:
    st.session_state.words = load_words()
    st.session_state.current_index = 0
    st.session_state.quiz_complete = False
    
    first_word = st.session_state.words[0]["english"]
    st.session_state.messages = [
        {"role": "assistant", "content": f"Welcome! Let's practice {len(st.session_state.words)} words today. Type the Hangul for: **{first_word}**"}
    ]

# 3. Draw the Chat UI
render_chat_history()

# 4. Handle User Input
if not st.session_state.quiz_complete:
    user_input = st.chat_input("Type in Hangul...")
    
    if user_input:
        # Show what the user typed
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        current_word = st.session_state.words[st.session_state.current_index]
        
        # Check if they are right
        with st.chat_message("assistant"):
            if check_answer(user_input, current_word):
                # Move to next word
                st.session_state.current_index += 1
                
                if st.session_state.current_index < len(st.session_state.words):
                    next_word_eng = st.session_state.words[st.session_state.current_index]["english"]
                    reply = f"Correct! 🎉 Next word: **{next_word_eng}**"
                else:
                    reply = "Awesome job! You finished your words for today. 🏆"
                    st.session_state.quiz_complete = True
            else:
                # Incorrect - give a hint
                reply = f"Not quite. Try again! \n\n*{get_hint(current_word)}*"
            
            # Save and display bot reply
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})