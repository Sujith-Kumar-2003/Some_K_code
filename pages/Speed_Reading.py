import streamlit as st
import streamlit.components.v1 as components
import json
import time

st.set_page_config(page_title="Speed Reading Tracker", page_icon="⏱️", layout="centered")

st.title("⏱️ Reading Speed Tracker")
st.markdown("Measure your natural reading flow. Read out loud, click 🔊 to check your pronunciation, and click **Done** when finished.")
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

if "last_selected_story" not in st.session_state:
    st.session_state.last_selected_story = selected_title
elif st.session_state.last_selected_story != selected_title:
    st.session_state.reading_state = "idle"
    st.session_state.last_selected_story = selected_title

# 4. Prepare the Text
selected_story = next(story for story in stories if story["title"] == selected_title)

pure_text = " ".join([page["korean"] for page in selected_story["pages"]])
word_count = len(pure_text.split())

if st.session_state.reading_state == "idle":
    st.info(f"**Length:** {word_count} words. The text is hidden until you start the timer.")

# --- CUSTOM HTML GENERATOR FOR TEXT-TO-SPEECH ---
def render_story_with_audio(story_pages):
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {
            margin: 0; padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: transparent;
        }
        .reading-text {
            font-size: 28px;
            line-height: 1.8;
            color: #333333;
            padding: 30px;
            background-color: #F8F9FA;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .sentence-block { margin-bottom: 25px; }
        .play-btn {
            background: none; border: none; font-size: 24px;
            cursor: pointer; vertical-align: middle; margin-left: 10px;
            transition: transform 0.2s;
        }
        .play-btn:hover { transform: scale(1.2); }
        @media (prefers-color-scheme: dark) {
            .reading-text { color: #E0E0E0; background-color: #1E1E1E; }
        }
    </style>
    </head>
    <body>
        <div class="reading-text">
    """
    
    # Add each sentence with its own play button
    for page in story_pages:
        safe_korean = page["korean"].replace("'", "\\'") # Prevent JS errors
        html_content += f"""
            <div class="sentence-block">
                {page["korean"]}
                <button class="play-btn" onclick="speak('{safe_korean}')" title="Listen to pronunciation">🔊</button>
            </div>
        """
        
    html_content += """
        </div>
        <script>
            window.speechSynthesis.onvoiceschanged = function() {
                window.speechSynthesis.getVoices();
            };
            function speak(text) {
                window.speechSynthesis.cancel();
                let utterance = new SpeechSynthesisUtterance(text + ".");
                utterance.lang = 'ko-KR'; 
                utterance.rate = 0.75; // Slightly slower for clear learning
                
                let voices = window.speechSynthesis.getVoices();
                let koreanVoices = voices.filter(v => v.lang.includes('ko'));
                if (koreanVoices.length > 0) {
                    let premiumVoice = koreanVoices.find(v => v.name.includes('Google') || v.name.includes('Premium') || v.name.includes('Siri'));
                    utterance.voice = premiumVoice ? premiumVoice : koreanVoices[0];
                }
                window.speechSynthesis.speak(utterance);
            }
        </script>
    </body>
    </html>
    """
    
    # Render the HTML component (500px high with a scrollbar so it fits nicely on screen)
    components.html(html_content, height=500, scrolling=True)
# ------------------------------------------------

# 5. Timer & Display Logic
if st.session_state.reading_state == "idle":
    if st.button("▶️ Start Timer & Reveal Text", type="primary", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.reading_state = "reading"
        st.rerun()

elif st.session_state.reading_state == "reading":
    
    render_story_with_audio(selected_story["pages"])
    
    if st.button("✅ I'm Done!", type="primary", use_container_width=True):
        end_time = time.time()
        st.session_state.time_taken = end_time - st.session_state.start_time
        
        if st.session_state.time_taken > 0:
            st.session_state.wpm_result = int((word_count / st.session_state.time_taken) * 60)
        else:
            st.session_state.wpm_result = 0
            
        st.session_state.reading_state = "finished"
        st.rerun()

elif st.session_state.reading_state == "finished":
    
    render_story_with_audio(selected_story["pages"])
    
    st.success(f"**Finished!** You read **{word_count} words** in **{st.session_state.time_taken:.1f} seconds**.")
    
    col1, col2 = st.columns(2)
    col1.metric("Your Reading Speed", f"{st.session_state.wpm_result} WPM")
    col2.metric("Time Elapsed", f"{st.session_state.time_taken:.1f} s")
    
    if st.button("🔄 Reset / Read Another", use_container_width=True):
        st.session_state.reading_state = "idle"
        st.rerun()