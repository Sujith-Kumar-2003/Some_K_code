import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Hangul Board", page_icon="🔈")
st.title("Hangul Reference Board 🔈")
st.markdown("Click any letter to hear its pronunciation! *(Make sure your device volume is up)*")

html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: Arial, sans-serif; }
    h3 { color: #333; margin-top: 20px; }
    .grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
    .btn { 
        padding: 15px; font-size: 24px; text-align: center; 
        background: #4A90E2; color: white; border-radius: 10px; 
        cursor: pointer; border: none; transition: 0.2s;
    }
    .btn:hover { background: #357ABD; }
    .label { font-size: 14px; display: block; margin-top: 5px; color: #e0e0e0; }
</style>
</head>
<body>
    <h3>Consonants</h3>
    <div class="grid">
        <button class="btn" onclick="speak('기역')">ㄱ<span class="label">g/k</span></button>
        <button class="btn" onclick="speak('니은')">ㄴ<span class="label">n</span></button>
        <button class="btn" onclick="speak('디귿')">ㄷ<span class="label">d/t</span></button>
        <button class="btn" onclick="speak('리을')">ㄹ<span class="label">r/l</span></button>
        <button class="btn" onclick="speak('미음')">ㅁ<span class="label">m</span></button>
        <button class="btn" onclick="speak('비읍')">ㅂ<span class="label">b/p</span></button>
        <button class="btn" onclick="speak('시옷')">ㅅ<span class="label">s</span></button>
        <button class="btn" onclick="speak('이응')">ㅇ<span class="label">ng</span></button>
        <button class="btn" onclick="speak('지읒')">ㅈ<span class="label">j</span></button>
        <button class="btn" onclick="speak('치읓')">ㅊ<span class="label">ch</span></button>
        <button class="btn" onclick="speak('키읔')">ㅋ<span class="label">k</span></button>
        <button class="btn" onclick="speak('티읕')">ㅌ<span class="label">t</span></button>
        <button class="btn" onclick="speak('피읖')">ㅍ<span class="label">p</span></button>
        <button class="btn" onclick="speak('히읗')">ㅎ<span class="label">h</span></button>
    </div>

    <h3>Vowels</h3>
    <div class="grid">
        <button class="btn" onclick="speak('아')">ㅏ<span class="label">a</span></button>
        <button class="btn" onclick="speak('야')">ㅑ<span class="label">ya</span></button>
        <button class="btn" onclick="speak('어')">ㅓ<span class="label">eo</span></button>
        <button class="btn" onclick="speak('여')">ㅕ<span class="label">yeo</span></button>
        <button class="btn" onclick="speak('오')">ㅗ<span class="label">o</span></button>
        <button class="btn" onclick="speak('요')">ㅛ<span class="label">yo</span></button>
        <button class="btn" onclick="speak('우')">ㅜ<span class="label">u</span></button>
        <button class="btn" onclick="speak('유')">ㅠ<span class="label">yu</span></button>
        <button class="btn" onclick="speak('으')">ㅡ<span class="label">eu</span></button>
        <button class="btn" onclick="speak('이')">ㅣ<span class="label">i</span></button>
    </div>

    <script>
        function speak(text) {
            let utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = 'ko-KR'; 
            window.speechSynthesis.speak(utterance);
        }
    </script>
</body>
</html>
"""
components.html(html_code, height=700, scrolling=True)