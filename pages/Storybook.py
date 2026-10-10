import streamlit as st
import streamlit.components.v1 as components
import json

st.set_page_config(page_title="Korean Storybook", page_icon="📚", layout="centered")

# Load stories from JSON
def load_stories():
    with open("data/stories.json", "r", encoding="utf-8") as file:
        return json.load(file)

stories = load_stories()

# Sidebar: Select a story
with st.sidebar:
    st.header("Library")
    story_titles = [story["title"] for story in stories]
    selected_title = st.selectbox("Choose a story:", story_titles)
    
    # Find the matching story data
    selected_story = next(story for story in stories if story["title"] == selected_title)
    
    # Reset to page 1 if the user switches books
    if "current_story" not in st.session_state or st.session_state.current_story != selected_title:
        st.session_state.current_story = selected_title
        st.session_state.book_page = 0

st.title(f"{selected_title} 📚")
story_pages = selected_story["pages"]

# Progress bar
st.progress((st.session_state.book_page + 1) / len(story_pages))

# Load current page
current = story_pages[st.session_state.book_page]

# Display Illustration
st.markdown(f"<h1 style='text-align: center; font-size: 120px; margin-bottom: 0px;'>{current['illustration']}</h1>", unsafe_allow_html=True)

# Display Korean Text
st.markdown(f"<h2 style='text-align: center; color: #4A90E2;'>{current['korean']}</h2>", unsafe_allow_html=True)

# Audio Button
audio_html = f"""
<div style="text-align: center; margin-bottom: 20px;">
    <button onclick="speak('{current['korean']}')" style="padding: 12px 24px; font-size: 18px; border-radius: 8px; background-color: #4A90E2; color: white; border: none; cursor: pointer; transition: 0.2s;">
        🔊 Read Aloud
    </button>
</div>
<script>
    function speak(text) {{
        let utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'ko-KR'; 
        window.speechSynthesis.speak(utterance);
    }}
</script>
"""
components.html(audio_html, height=80)

# Expandable Translation
with st.expander("Show Translation & Romanization"):
    st.markdown(f"**Romanization:** {current['romanization']}")
    st.markdown(f"**English:** {current['english']}")

st.divider()

# Navigation Buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.session_state.book_page > 0:
        if st.button("⬅️ Previous", use_container_width=True):
            st.session_state.book_page -= 1
            st.rerun()

with col3:
    if st.session_state.book_page < len(story_pages) - 1:
        if st.button("Next ➡️", use_container_width=True):
            st.session_state.book_page += 1
            st.rerun()