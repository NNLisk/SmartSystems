import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("WARNING: GEMINI_API_KEY not found in .env file!")

genai.configure(api_key=API_KEY)

# Use one of the available models from your list
model = genai.GenerativeModel("gemini-2.5-flash")

async def get_funny_day_rating(attendance, lectures, weather, lunch):
    if not API_KEY:
        return " AI advisor unavailable (no API key configured)"
    
    prompt = f"""
You are a humorous assistant. Based on the user's data, create ONE funny verdict sentence/recommendation if the user should stay at home or go to university campus

Do not be serious.

DATA:
- Past attendance: {attendance}
- Today's lectures: {lectures}
- Weather today: {weather}
- Lunch menu: {lunch}

Rules:
- Very short 1 sentence.
- FUNNY, base the humor ONLY on the summary I provide.
- Highlight one or two things from data (your choice) in abstract way.
- Very obviously not serious
- if applicable give a tip for very bad weather
"""
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f" AI humor failed: {str(e)}"