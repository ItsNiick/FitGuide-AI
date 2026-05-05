import streamlit as st
from workout_ai import generate_workout

st.set_page_config(
    page_title="FitGuide AI",
    page_icon="💪",
    layout="centered"
)

st.title("Welcome to FitGuide AI")
st.subheader("Personalzied Workout Routine Assistant")

st.write("Answer a few questions to get a personalized workout routine.")

with st.form("workout_form"):
    goal = st.selectbox(
        "What is your main fitness goal?",
        ["Strength", "Muscle Gain", "Weight Loss", "Endurance", "Flexibility", "General Fitness"]
    )

    experience = st.selectbox(
        "What is your experience level?",
        ["Beginner", "Intermediate", "Advanced"]
    )

    time = st.selectbox(
        "How much time do you have for workouts?",
        ["15 Minutes", "30 Minutes", "45 Minutes", "60 Minutes", "More than 60 Minutes"]
    )

    equipment = st.multiselect(
        "What equipment do you have access to?",
        ["None", "Dumbbells", "Barbell", "Resistance Bands", "Kettlebells", "Full Gym"]
    )

    soreness = st.selectbox(
        "How sore or fatigued are you today?",
        ["Low", "Medium", "High"]
    )

    preference = st.selectbox(
        "What type of workout do you prefer?",
        ["Strength", "Cardio", "Mixed", "Mobility/Flexibility", "No Preference"]
    )

    limitations = st.text_area(
        "Do you have any injuries or limitations we should consider?",
        placeholder="Example: Knee pain, lower back issues, etc."
    )

    submitted = st.form_submit_button("Generate Workout")

if submitted:
    user_profile = {
        "goal": goal,
        "experience": experience,
        "time": time,
        "equipment": equipment,
        "soreness": soreness,
        "limitations": limitations if limitations else "None",
        "preference": preference
    }

    with st.spinner("Generating your workout routine..."):
        workout = generate_workout(user_profile)

    st.success("Workout Generated.")
    st.markdown("## Your Personalized Workout Routine")
    st.markdown(workout)