import os
import json
from dotenv import load_dotenv
from google import genai
import streamlit as st

load_dotenv()

def get_api_key():
    try:
        return st.secrets["GOOGLE_API_KEY"]
    except Exception:
        return os.getenv("GOOGLE_API_KEY")
    
api_key = get_api_key()

if not api_key:
    raise ValueError("GOOGLE_API_KEY is not set. Add it to Streamlit Secrets or your .env file.")

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_workout(user_profile):
    prompt = f"""
You are FitGuide AI, a safe and beginner-friendly workout assistant.

Create a personalized workout routine based on this user profile:

Goal: {user_profile["goal"]}
Experience level: {user_profile["experience"]}
Available time: {user_profile["time"]}
Equipment: {user_profile["equipment"]}
Soreness/fatigue: {user_profile["soreness"]}
Limitations/injuries: {user_profile["limitations"]}
Workout preference: {user_profile["preference"]}

Return ONLY valid JSON in this exact structure:

{{
  "title": "Workout title",
  "warmup": [
    "Warm-up task 1",
    "Warm-up task 2",
    "Warm-up task 3"
  ],
  "exercises": [
    {{
      "name": "Exercise name",
      "sets": "Number of sets",
      "reps": "Reps or time",
      "rest": "Rest period"
    }}
  ],
  "cooldown": [
    "Cooldown task 1",
    "Cooldown task 2",
    "Cooldown task 3"
  ],
  "explanation": "Brief explanation of why this workout fits the user.",
  "disclaimer": "Short safety disclaimer."
}}

Rules:
- Include 3 warm-up tasks
- Include 4-6 exercises
- Include 3 cooldown tasks
- Keep the routine realistic for the user's available time
- If soreness is high, make it lower intensity
- If the user reports pain or injury, avoid intense exercises and suggest consulting a professional
- Do not include markdown
- Do not include text outside the JSON
- Always include a disclaimer at the end that I am not a doctor but instead an extension of Google Gemini designed by Nicholas Shedd, and that not all information may be correct for you and your fitness goals.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {
            "title": "Workout Generated",
            "warmup": [],
            "exercises": [],
            "cooldown": [],
            "explanation": response.text,
            "disclaimer": "This is general fitness guidance, not medical advice."
        }