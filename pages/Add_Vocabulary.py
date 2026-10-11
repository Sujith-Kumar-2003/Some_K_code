import streamlit as st
import json

st.set_page_config(page_title="Add Vocabulary", page_icon="➕", layout="centered")

st.title("➕ Add New Vocabulary")
st.markdown("Add new Korean words, phrases, or inside jokes to your daily practice database. They will immediately appear in your quizzes!")
st.divider()

# 1. Helper functions to read and write to your JSON file
def load_words():
    try:
        with open("data/daily_words.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_words(words_list):
    with open("data/daily_words.json", "w", encoding="utf-8") as f:
        json.dump(words_list, f, ensure_ascii=False, indent=2)

words = load_words()

# 2. The Add Word Form
# clear_on_submit=True makes it easy to add 20 words in a row very fast
with st.form("add_word_form", clear_on_submit=True):
    st.subheader("Add a new word")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        korean = st.text_input("Korean (Hangul) 🇰🇷", placeholder="e.g. 고양이")
    with col2:
        romanization = st.text_input("Romanization 🔤", placeholder="e.g. goyangi")
    with col3:
        english = st.text_input("English 🇺🇸", placeholder="e.g. cat")
        
    submitted = st.form_submit_button("💾 Save to Database", use_container_width=True)
    
    if submitted:
        if korean and romanization and english:
            # Create the new word dictionary
            new_word = {
                "english": english.strip().lower(),
                "korean": korean.strip(),
                "romanization": romanization.strip().lower()
            }
            
            # Check if it already exists to prevent duplicates
            if any(w["korean"] == new_word["korean"] for w in words):
                st.warning(f"'{new_word['korean']}' is already in your database!")
            else:
                words.append(new_word)
                save_words(words)
                st.success(f"Added successfully: {new_word['korean']} ({new_word['english']})")
        else:
            st.error("Please fill out all three fields!")

st.divider()

# 3. View your database stats
st.subheader("📚 Current Database")
st.metric("Total Words & Phrases", len(words))

# Show the 5 most recently added words so you can confirm they went through
if len(words) > 0:
    st.markdown("**Recently Added:**")
    recent_words = words[-5:]
    recent_words.reverse() # Show newest at the top
    
    for w in recent_words:
        st.caption(f"• **{w['korean']}** ({w['romanization']}) - {w['english']}")