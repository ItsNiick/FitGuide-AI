import streamlit as st
from PIL import Image
from workout_ai import generate_workout

icon = Image.open("images/tts.jpeg")

st.set_page_config(
    page_title="FitGuide AI",
    page_icon=icon,
    layout="centered"
)

# Creates a session state initialization
if "workout" not in st.session_state:
    st.session_state.workout = None

if "last_user_profile" not in st.session_state:
    st.session_state.last_user_profile = None


# Cached the Gemini call
# I previously had a problem where the workout would regenerate every time the user checked a box
# Which resulted in me using all of my free tokens in one workout session.
@st.cache_data(show_spinner=False)
def cached_generate_workout(goal, experience, time, equipment, soreness, limitations, preference):
    user_profile = {
        "goal": goal,
        "experience": experience,
        "time": time,
        "equipment": list(equipment),
        "soreness": soreness,
        "limitations": limitations,
        "preference": preference
    }

    return generate_workout(user_profile)


# Page UI
# (Thank God for Streamlit, I suck at frontend design)
st.title("Welcome to FitGuide AI")
st.subheader("Personalized Workout Routine Assistant")

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



# Only generate when button is clicked
if submitted:
    clean_equipment = tuple(equipment) if equipment else ("None",)
    clean_limitations = limitations if limitations else "None"

    st.session_state.last_user_profile = {
        "goal": goal,
        "experience": experience,
        "time": time,
        "equipment": clean_equipment,
        "soreness": soreness,
        "limitations": clean_limitations,
        "preference": preference
    }

    with st.spinner("Generating your workout routine..."):
        st.session_state.workout = cached_generate_workout(
            goal,
            experience,
            time,
            clean_equipment,
            soreness,
            clean_limitations,
            preference
        )


# Display saved workout
# This stays even after checkboxes are ticked off
if st.session_state.workout is not None:
    workout = st.session_state.workout

    st.markdown("## Your Personalized Workout Routine")
    st.success("Workout Generated.")

    st.markdown(f"## {workout['title']}")

    st.markdown("### Warm-Up")
    for i, task in enumerate(workout["warmup"]):
        st.checkbox(task, key=f"warmup_{i}")

    st.markdown("### Main Workout")
    for i, exercise in enumerate(workout["exercises"]):
        label = f"{exercise['name']} — {exercise['sets']} sets x {exercise['reps']} | Rest: {exercise['rest']}"
        st.checkbox(label, key=f"exercise_{i}")

    st.markdown("### Cooldown")
    for i, task in enumerate(workout["cooldown"]):
        st.checkbox(task, key=f"cooldown_{i}")

    # Cool Progress bar
    total_tasks = (
        len(workout["warmup"]) +
        len(workout["exercises"]) +
        len(workout["cooldown"])
    )

    completed_tasks = 0

    for i in range(len(workout["warmup"])):
        if st.session_state.get(f"warmup_{i}", False):
            completed_tasks += 1

    for i in range(len(workout["exercises"])):
        if st.session_state.get(f"exercise_{i}", False):
            completed_tasks += 1

    for i in range(len(workout["cooldown"])):
        if st.session_state.get(f"cooldown_{i}", False):
            completed_tasks += 1

    st.markdown("### Workout Progress")
    st.progress(completed_tasks / total_tasks)
    st.write(f"{completed_tasks}/{total_tasks} tasks completed")

    st.markdown("### Why This Workout Fits You")
    st.write(workout["explanation"])

    st.info(workout["disclaimer"])