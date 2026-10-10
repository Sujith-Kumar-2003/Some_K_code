import json
import streamlit as st
import difflib
import random
import re
from streamlit_mic_recorder import speech_to_text

# 1. Page Configuration & Custom CSS
st.set_page_config(page_title="Korean Daily Practice", page_icon="🇰🇷", layout="centered")

st.markdown("""
    <style>
    .big-korean {
        font-size: 45px !important;
        font-weight: bold;
        color: #4A90E2;
        text-align: center;
        margin: 10px 0px;
    }
    .hint-text {
        color: #888888;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🇰🇷 Daily Korean Practice")
st.markdown("Test your Hangul reading skills! Type the romanization/English, OR tap the mic to speak the Korean word.")
st.divider()

# 2. Logic Functions
def load_words(filepath="data/daily_words.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def check_answer(user_input, current_word):
    # FIRST CHECK: If the user spoke via mic, it will output Hangul. Check if it matches exactly.
    if user_input.strip() == current_word['korean']:
        return 1.0

    # SECOND CHECK: Fallback to the typing logic (romanization + english)
    clean_user = " ".join(user_input.replace("/", " ").lower().split())
    clean_target = f"{current_word['romanization'].lower()} {current_word['english'].lower()}"
    clean_target = " ".join(clean_target.split())
    
    return difflib.SequenceMatcher(None, clean_user, clean_target).ratio()

def get_hint(current_word):
    first_letter = current_word["romanization"][0].lower()
    return f"<span class='hint-text'>💡 Hint: Type both! Format it like '{first_letter}... / {current_word['english'].lower()}' or just use a space!</span>"

def render_chat_history():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)

# 3. Sidebar UI
with st.sidebar:
    st.header("📊 Your Progress")
    
    current = st.session_state.get("current_index", 0)
    total_words = len(st.session_state.get("words", []))
    
    st.metric(label="Words Completed", value=f"{current} / {total_words}" if total_words > 0 else "0 / 0")
    st.progress(current / total_words if total_words > 0 else 0)
    
    st.divider()
    st.header("⚙️ Controls")
    
    if st.button("🔄 Restart & Shuffle Quiz", use_container_width=True, type="primary"):
        st.session_state.clear()
        st.rerun()

# 4. Initialize Session State
if "words" not in st.session_state:
    all_words = load_words()
    random.shuffle(all_words)
    st.session_state.words = all_words
    
    st.session_state.current_index = 0
    st.session_state.quiz_complete = False
    
    first_word = st.session_state.words[0]["korean"]
    st.session_state.messages = [
        {"role": "assistant", "content": f"Welcome! Let's practice {len(st.session_state.words)} words today.\n\n**Rule:** Type the romanization AND the english, OR use the mic to speak in Korean!\n\n<div class='big-korean'>{first_word}</div>"}
    ]

# 5. Draw the Chat UI
render_chat_history()

# 6. Handle User Input
if not st.session_state.quiz_complete:
    
    # 6a. Voice Input Component (Sits right above the chat input)
    st.markdown("🎙️ **Or speak the word:**")
    voice_input = speech_to_text(language='ko-KR', use_container_width=True, just_once=True, key='STT')
    
    # 6b. Text Input Component
    text_input = st.chat_input("Type 'romanization / english' or 'romanization english'...")
    
    # 6c. Combine inputs (Use whatever they interacted with)
    user_input = text_input or voice_input
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
            
        current_word = st.session_state.words[st.session_state.current_index]
        
        with st.chat_message("assistant"):
            similarity = check_answer(user_input, current_word)
            
            if similarity >= 0.80:
                st.session_state.current_index += 1
                
                exact_answer = f"{current_word['romanization']} / {current_word['english']}".lower()
                
                if similarity == 1.0:
                    # If they spoke it perfectly in Korean, acknowledge that!
                    if user_input.strip() == current_word['korean']:
                        prefix = "✅ **Perfect Pronunciation!** 🎙️🎉"
                    else:
                        prefix = "✅ **Correct!** 🎉"
                else:
                    prefix = f"⚠️ **Close enough!** Nice try, but the exact spelling is **{exact_answer}**."
                
                if st.session_state.current_index < len(st.session_state.words):
                    next_word_kor = st.session_state.words[st.session_state.current_index]["korean"]
                    reply = f"{prefix}\n\nNext word:\n<div class='big-korean'>{next_word_kor}</div>"
                else:
                    reply = f"{prefix}\n\n**Awesome job! You finished all your words for today.** 🏆"
                    st.session_state.quiz_complete = True
                    st.balloons() 
            else:
                reply = f"❌ **Not quite. Try again!** \n\n{get_hint(current_word)}"
            
            st.markdown(reply, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": reply})
            
            st.rerun()