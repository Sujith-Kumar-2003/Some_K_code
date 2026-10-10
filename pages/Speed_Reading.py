import streamlit as st
import json
import time

st.set_page_config(page_title="Speed Reading Tracker", page_icon="⏱️", layout="centered")

# Custom CSS to make the paragraph highly readable
st.markdown("""
    <style>
    .reading-text {
        font-size: 28px !important;
        line-height: 1.8;
        color: #333333;
        padding: 30px;
        background-color: #F8F9FA;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .reading-text {
            color: #E0E0E0;
            background-color: #1E1E1E;
        }
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⏱️ Reading Speed Tracker")
st.markdown("Measure your natural reading flow. Start the timer, read at your own pace, and click **Done**.")
st.divider()

# 1. Load Stories
def load_stories():
    try:
        with open("data/stories.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

stories = load_stories()

if not stories:
    st.warning("No stories found. Please make sure data/stories.json exists.")
    st.stop()

# 2. Setup Session State for the Timer
if "reading_state" not in st.session_state:
    st.session_state.reading_state = "idle" 
if "start_time" not in st.session_state:
    st.session_state.start_time = 0
if "wpm_result" not in st.session_state:
    st.session_state.wpm_result = 0
if "time_taken" not in st.session_state:
    st.session_state.time_taken = 0

# 3. Story Selection UI
story_titles = [story["title"] for story in stories]
selected_title = st.selectbox("Choose a story to read:", story_titles, disabled=(st.session_state.reading_state == "reading"))

# Reset the timer state if you pick a different book
if "last_selected_story" not in st.session_state:
    st.session_state.last_selected_story = selected_title
elif st.session_state.last_selected_story != selected_title:
    st.session_state.reading_state = "idle"
    st.session_state.last_selected_story = selected_title

# 4. Prepare the Text
selected_story = next(story for story in stories if story["title"] == selected_title)

# Calculate word count purely from the words
pure_text = " ".join([page["korean"] for page in selected_story["pages"]])
word_count = len(pure_text.split())

# Format the display text to have line breaks between each sentence!
display_korean_text = "<br><br>".join([page["korean"] for page in selected_story["pages"]])

if st.session_state.reading_state == "idle":
    st.info(f"**Length:** {word_count} words. The text is hidden until you start the timer.")

# 5. Timer & Display Logic
if st.session_state.reading_state == "idle":
    if st.button("▶️ Start Timer & Reveal Text", type="primary", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.reading_state = "reading"
        st.rerun()

elif st.session_state.reading_state == "reading":
    # Show the spaced-out text
    st.markdown(f"<div class='reading-text'>{display_korean_text}</div>", unsafe_allow_html=True)
    
    if st.button("✅ I'm Done!", type="primary", use_container_width=True):
        end_time = time.time()
        st.session_state.time_taken = end_time - st.session_state.start_time
        
        # Calculate WPM: (Total Words / Seconds Taken) * 60
        if st.session_state.time_taken > 0:
            st.session_state.wpm_result = int((word_count / st.session_state.time_taken) * 60)
        else:
            st.session_state.wpm_result = 0
            
        st.session_state.reading_state = "finished"
        st.rerun()

elif st.session_state.reading_state == "finished":
    # Keep showing the text so you can review it
    st.markdown(f"<div class='reading-text'>{display_korean_text}</div>", unsafe_allow_html=True)
    
    # Display the results
    st.success(f"**Finished!** You read **{word_count} words** in **{st.session_state.time_taken:.1f} seconds**.")
    
    col1, col2 = st.columns(2)
    col1.metric("Your Reading Speed", f"{st.session_state.wpm_result} WPM")
    col2.metric("Time Elapsed", f"{st.session_state.time_taken:.1f} s")
    
    if st.button("🔄 Reset / Read Another", use_container_width=True):
        st.session_state.reading_state = "idle"
        st.rerun()