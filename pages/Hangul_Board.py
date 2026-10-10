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

    <h3>Consonants</h3>
    <div class="grid">
        <button class="btn" onclick="speak('그')">ㄱ<span class="label">g/k</span></button>
        <button class="btn" onclick="speak('느')">ㄴ<span class="label">n</span></button>
        <button class="btn" onclick="speak('드')">ㄷ<span class="label">d/t</span></button>
        <button class="btn" onclick="speak('르')">ㄹ<span class="label">r/l</span></button>
        <button class="btn" onclick="speak('므')">ㅁ<span class="label">m</span></button>
        <button class="btn" onclick="speak('브')">ㅂ<span class="label">b/p</span></button>
        <button class="btn" onclick="speak('스')">ㅅ<span class="label">s</span></button>
        <button class="btn" onclick="speak('으')">ㅇ<span class="label">ng</span></button>
        <button class="btn" onclick="speak('즈')">ㅈ<span class="label">j</span></button>
        <button class="btn" onclick="speak('츠')">ㅊ<span class="label">ch</span></button>
        <button class="btn" onclick="speak('크')">ㅋ<span class="label">k</span></button>
        <button class="btn" onclick="speak('트')">ㅌ<span class="label">t</span></button>
        <button class="btn" onclick="speak('프')">ㅍ<span class="label">p</span></button>
        <button class="btn" onclick="speak('흐')">ㅎ<span class="label">h</span></button>
    </div>
    <h3>Double Consonants</h3>
        <div class="grid">
            <button class="btn" onclick="speak('끄')">ㄲ<span class="label">kk</span></button>
            <button class="btn" onclick="speak('뜨')">ㄸ<span class="label">tt</span></button>
            <button class="btn" onclick="speak('쁘')">ㅃ<span class="label">pp</span></button>
            <button class="btn" onclick="speak('쓰')">ㅆ<span class="label">ss</span></button>
            <button class="btn" onclick="speak('쯔')">ㅉ<span class="label">jj</span></button>
        </div>

        <h3>Complex Vowels</h3>
        <div class="grid">
            <button class="btn" onclick="speak('애')">ㅐ<span class="label">ae</span></button>
            <button class="btn" onclick="speak('얘')">ㅒ<span class="label">yae</span></button>
            <button class="btn" onclick="speak('에')">ㅔ<span class="label">e</span></button>
            <button class="btn" onclick="speak('예')">ㅖ<span class="label">ye</span></button>
            <button class="btn" onclick="speak('와')">ㅘ<span class="label">wa</span></button>
            <button class="btn" onclick="speak('왜')">ㅙ<span class="label">wae</span></button>
            <button class="btn" onclick="speak('외')">ㅚ<span class="label">oe</span></button>
            <button class="btn" onclick="speak('워')">ㅝ<span class="label">wo</span></button>
            <button class="btn" onclick="speak('웨')">ㅞ<span class="label">we</span></button>
            <button class="btn" onclick="speak('위')">ㅟ<span class="label">wi</span></button>
            <button class="btn" onclick="speak('의')">ㅢ<span class="label">ui</span></button>
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