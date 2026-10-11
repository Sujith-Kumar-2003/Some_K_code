# 🇰🇷 Daily Korean Practice App

A personalized, interactive web application built with Streamlit and Python to help users practice reading Hangul, expand their vocabulary, and improve their reading speed.

## 🚀 Features

*   **Interactive Vocabulary Quizzes:** Tests your ability to recognize Hangul. You can answer using romanization, English translation, or both.
*   **🎙️ Voice Recognition Support:** Practice your pronunciation! Use the built-in microphone tool to speak the Korean word directly. If your pronunciation matches, you pass the word instantly.
*   **⏱️ Speed Reading Tracker:** Level up from sounding out letters to instant word recognition. Read Korean short stories at your own pace and automatically track your Words Per Minute (WPM).
*   **Flexible Grading System:** The app features a fuzzy-matching grading system that tolerates minor typos and normalizes spacing (e.g., `uyu / milk` vs `uyu milk`).
*   **Custom Database Entry:** Includes an easy-to-use "Add Vocabulary" page to rapidly add new words or phrases to your JSON database directly from the app.
*   **Sleek UI:** Custom CSS scaling for easy-to-read Hangul characters, built-in progress bars, and celebration animations upon completing daily tasks.

## 🛠️ Technology Stack

*   **Frontend & Framework:** [Streamlit](https://streamlit.io/)
*   **Language:** Python 3
*   **Voice Integration:** `streamlit-mic-recorder`
*   **Data Storage:** Local JSON (`data/daily_words.json`, `data/stories.json`)

## 📦 Installation & Setup

If you want to run this app locally on your own machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Sujith-Kumar-2003/Some_K_code.git](https://github.com/Sujith-Kumar-2003/Some_K_code.git)
    cd Some_K_code
    ```

2.  **Install the required dependencies:**
    Make sure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

```text
├── app.py                      # Main quiz application and navigation
├── pages/
│   ├── Add_Vocabulary.py       # Data entry form for new words
│   ├── Speed_Reading.py        # WPM tracker and paragraph reading tool
│   └── Storybook.py            # Interactive children's storybook reader
├── data/
│   ├── daily_words.json        # Core vocabulary database
│   └── stories.json            # Short stories for speed reading
├── .github/workflows/
│   └── keep-alive.yml          # GitHub Action to keep Streamlit Cloud awake
└── requirements.txt            # Python dependencies
