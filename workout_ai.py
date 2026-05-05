import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

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

Requirements:
- Include a warm-up
- Include 4-6 main exercises
- Include sets, reps, or time
- Include rest periods
- Include a cooldown
- Explain why this workout fits the user
- Keep the routine realistic for the available time
- If soreness is high, recommend a lower-intensity workout
- If the user reports pain or injury, avoid intense exercises and suggest consulting a professional
- Do not make medical claims
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    return response.text