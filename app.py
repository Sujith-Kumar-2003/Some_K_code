import json
import streamlit as st

# 1. Page Configuration
st.set_page_config(page_title="Korean Daily Practice", page_icon="🇰🇷")
st.title("Daily Korean Practice 🇰🇷")

# 2. Logic Functions (Directly in app.py to prevent caching desync)
def load_words(filepath="data/daily_words.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def check_answer(user_input, current_word):
    # Case-insensitive comparison against the romanized English spelling
    return user_input.strip().lower() == current_word["romanization"].lower()

def get_hint(current_word):
    first_letter = current_word["romanization"][0]
    return f"Hint: The Hangul is '{current_word['korean']}' and the english spelling starts with '{first_letter}'"

def render_chat_history():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# 3. Sidebar Reset Button
with st.sidebar:
    st.header("Controls")
    if st.button("Restart Quiz"):
        st.session_state.clear()
        st.rerun()

# 4. Initialize Session State
if "words" not in st.session_state:
    st.session_state.words = load_words()
    st.session_state.current_index = 0
    st.session_state.quiz_complete = False
    
    first_word = st.session_state.words[0]["english"]
    st.session_state.messages = [
        {"role": "assistant", "content": f"Welcome! Let's practice {len(st.session_state.words)} words today. Type the romanization (english spelling) for: **{first_word}**"}
    ]

# 5. Draw the Chat UI
render_chat_history()

# 6. Handle User Input
if not st.session_state.quiz_complete:
    user_input = st.chat_input("Type in english...")
    
    if user_input:
        # Display user input
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        current_word = st.session_state.words[st.session_state.current_index]
        
        # Verify answer
        with st.chat_message("assistant"):
            if check_answer(user_input, current_word):
                st.session_state.current_index += 1
                
                if st.session_state.current_index < len(st.session_state.words):
                    next_word_eng = st.session_state.words[st.session_state.current_index]["english"]
                    reply = f"Correct! 🎉 Next word: **{next_word_eng}**"
                else:
                    reply = "Awesome job! You finished your words for today. 🏆"
                    st.session_state.quiz_complete = True
            else:
                reply = f"Not quite. Try again! \n\n*{get_hint(current_word)}*"
            
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})