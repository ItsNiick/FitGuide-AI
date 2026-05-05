from workout_ai import generate_workout

def main():
    print("Welcome to FitGuide AI!")
    print("Answer a few questions to get a personalized workout.\n")

    user_profile = {
        "goal": input("Fitness goal: "),
        "experience": input("Experience level: "),
        "time": input("Available time: "),
        "equipment": input("Equipment available: "),
        "soreness": input("Soreness/fatigue level: "),
        "limitations": input("Any injuries or limitations? "),
        "preference": input("Workout preference: ")
    }

    print("\nGenerating your workout...\n")

    workout = generate_workout(user_profile)

    print("Your Personalized Workout Routine")
    print("--------------------------------")
    print(workout)

if __name__ == "__main__":
    main()