import json
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY_REMOVED")
model = genai.GenerativeModel('gemini-2.5-flash')

prompt = """
Generate 40 short beginner-level Korean stories in JSON format. 
Each story must follow this exact schema:
[
  {
    "title": "Story Title (with 1 emoji)",
    "pages": [
      { 
        "illustration": "2 emojis", 
        "korean": "Korean sentence using formal polite (-습니다/합니다) form", 
        "romanization": "accurate lowercase romanization", 
        "english": "English translation" 
      }
    ]
  }
]
Each story should have 2 to 3 pages. Keep vocabulary simple. Output ONLY valid JSON, no markdown formatting.
"""

print("Generating stories... (this might take a minute)")
response = model.generate_content(prompt)

try:
    # Clean the response to ensure valid JSON
    new_stories_json = response.text.replace("```json", "").replace("```", "").strip()
    new_stories = json.loads(new_stories_json)
    
    # Load your existing stories
    with open("data/stories.json", "r", encoding="utf-8") as file:
        existing_stories = json.load(file)
        
    # Combine and save
    existing_stories.extend(new_stories)
    
    with open("data/stories.json", "w", encoding="utf-8") as file:
        json.dump(existing_stories, file, ensure_ascii=False, indent=2)
        
    print(f"Success! Added {len(new_stories)} new stories to data/stories.json")

except Exception as e:
    print(f"Error parsing JSON: {e}")