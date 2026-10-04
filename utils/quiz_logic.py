import json

def load_words(filepath="data/daily_words.json"):
    """Loads the daily vocabulary from the JSON file."""
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def check_answer(user_input, current_word):
    """Returns True if the user's Hangul perfectly matches the answer."""
    return user_input.strip() == current_word["korean"]

def get_hint(current_word):
    """Formats the romanization hint."""
    return f"Hint: The romanization is '{current_word['romanization']}'"