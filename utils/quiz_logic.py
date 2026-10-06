import json

def load_words(filepath="data/daily_words.json"):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def check_answer(user_input, current_word):
    return user_input.strip().lower() == current_word["romanization"].lower()

def get_hint(current_word):
    first_letter = current_word["romanization"][0]
    return f"Hint: The Hangul is '{current_word['korean']}' and the english spelling starts with '{first_letter}'"