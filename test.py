import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# --- Setup ---
st.set_page_config(page_title="Helios Towers Python Game", layout="centered")

if "username" not in st.session_state:
    st.session_state.username = ""
if "game_stage" not in st.session_state:
    st.session_state.game_stage = 0
if "score" not in st.session_state:
    st.session_state.score = 0

# --- Game config ---
correct_answers = ["14", "TZDA0143", "17", "59.5"]  # Add more correct answers as needed

# --- Page 1: Enter username ---
if st.session_state.username == "":
    st.title("🏗️ Welcome to the Helios Towers Python Challenge!")
    st.markdown("Enter your name to begin the adventure:")
    username = st.text_input("Your nickname or name")

    if username:
        st.session_state.username = username
        st.rerun()

else:
    st.sidebar.title(f"🎮 Player: {st.session_state.username}")
    st.sidebar.markdown(f"**Progress:** Game {st.session_state.game_stage + 1} of 4")
    st.sidebar.markdown(f"**Score:** {st.session_state.score} ⭐")

    # === GAME 1 ===
    if st.session_state.game_stage == 0:
        st.header("⛽ Game 1: Fuel Tracker")
        st.image(
            "https://i.imgur.com/KI7XgUb.png", width=400
        )  # Replace with your image

        st.markdown(
            """
        A generator's fuel log over the last 24 hours shows a strange pattern.

        🔍 Use Python to plot the fuel consumption and find the suspicious hour.

        **Copy and paste this prompt into ChatGPT:**
        ```
        I'm analyzing hourly fuel consumption for a generator site.

        Write Python code using pandas and matplotlib to:

        1. Create a DataFrame for the last 24 hours of consumption.
        2. Use this static data (in liters):
           [2.42, 2.48, 2.51, 2.47, 2.44, 2.50, 2.53, 2.45, 2.49, 2.52, 2.46, 2.50,
            2.43, 2.55, 5.82, 2.48, 2.51, 2.47, 2.49, 2.53, 2.46, 2.44, 2.50, 2.49]

        3. Plot a line chart with:
           - x-axis = hour (0 to 23)
           - y-axis = consumption (liters)
           - Add markers to each point

        4. Visually identify which hour might be an anomaly in the fuel pattern.
        ```
        """
        )

        answer = st.text_input("Which hour shows an anomaly?").strip()
        if st.button("Submit"):
            if answer == correct_answers[0]:
                st.success("Correct! That spike was suspicious indeed! ⛽🚨")
                st.balloons()
                st.session_state.score += 1
                st.session_state.game_stage += 1
                st.rerun()
            else:
                st.error("Hmm, not quite. Look at that spike again!")

    # === GAME 2 ===
    elif st.session_state.game_stage == 1:
        st.title("🧠 Game 2: The Mystery of the Missing Fuel")

        st.markdown(
            """
            One of your sites has unusual fuel consumption, and the Field Engineer suspects something’s off.
            
            You have the last 7 days of fuel data (in liters):

            ```python
            [88, 91, 85, 300, 89, 87, 90]
            ```

            But your boss doesn’t have time to check it — they told you:

            > "`Please help me analyze the fuel consumption data The data set is [88, 91, 85, 300, 89, 87, 90]. Anything unusual?`"
            """
        )

        st.info(
            "👀 Tip: Open ChatGPT, paste the data and the prompt above, and see what it tells you."
        )

        user_answer = st.text_input(
            "What did you find out from ChatGPT? (Keep it short)", ""
        ).strip()

        # Keywords that indicate the user spotted the anomaly
        success_keywords = ["day 4", "300", "anomaly", "spike", "suspicious", "unusual"]

        if st.button("Submit Game 2"):
            if any(keyword in user_answer.lower() for keyword in success_keywords):
                st.success(
                    "✅ Correct! Day 4 stands out with 300 liters — great job using ChatGPT for analysis."
                )
                st.session_state.score += 1
                st.session_state.game_stage += 1
                st.balloons()
                st.rerun()
            else:
                st.warning(
                    "Hmm... that doesn't seem quite right. Try prompting ChatGPT with the data!"
                )

    # === GAME 3 ===
    elif st.session_state.game_stage == 2:
        st.header("🏙️ Game 3: Rent Race — Prompt Your Way to the Top")
        st.image("https://i.imgur.com/N2dztxz.png", width=400)

        st.markdown(
            """
            Helios is reviewing lease rates across regions.

            You're given simulated data for 3 regions:
            - **Bas-Congo**: 3500, 4200, 3900
            - **Kinshasa**: 4400, 4100, 4300
            - **Equateur**: 3600, 3700, 3650

            Your boss tells you:

            > *“Use ChatGPT to figure out which region has the highest **average lease rate**. Just tell it what you want — no need to write code yourself!”*

            ---
            👇 Example Prompt You Could Use:
            > *“I have lease rates for 3 regions. Can you calculate the average for each and tell me which one is highest?”*

            You can also copy this sample message:
            ```
            I have lease rates for 3 regions:
            Bas-Congo: 3500, 4200, 3900
            Kinshasa: 4400, 4100, 4300
            Equateur: 3600, 3700, 3650
            Which region has the highest average lease rate?
            ```

            🧠 **Hint**: It's not about memorizing — it's about clearly communicating with ChatGPT.
            """
        )

        answer = st.text_input("Which region has the highest average lease rate?")
        if st.button("Submit Game 3"):
            if answer.strip().lower() == "kinshasa":
                st.success("📈 Correct! Kinshasa pays the premium 💰")
                st.session_state.score += 1
                st.session_state.game_stage += 1
                st.rerun()
            else:
                st.error("That's not the top payer. Try your prompt again!")

    # === GAME 4 ===
    elif st.session_state.game_stage == 3:
        st.header("🏗️ Game 4: Build the 3D Tower")
        st.image("https://i.imgur.com/xuwKQ6y.jpeg", width=400)

        st.markdown(
            """
        Let’s visualize your dream tower in 3D with alternating red and white segments.

        **Copy this prompt into ChatGPT:**
        ```
        Use Plotly in Python to create a 3D tower with 6 stacked cylinders.
        - Each 10m high
        - Alternate red and white
        - Use go.Cylinder or go.Mesh3d if available
        Label each segment
        ```
        """
        )

        answer = st.text_input("What is the total height of your tower?")
        if st.button("Submit Final Game"):
            if answer == correct_answers[3]:
                st.success("You did it! You’ve built the tower of the future! 🚀")
                st.session_state.score += 1
                st.session_state.game_stage += 1
                st.rerun()
            else:
                st.error("Almost there! Double-check your output height.")

    # === COMPLETED ===
    else:
        st.success("🎉 You’ve completed all 4 challenges!")
        st.markdown(f"**Total Score:** {st.session_state.score}/4 ⭐")
        st.balloons()

        st.markdown("Want to play again?")
        if st.button("Restart Game"):
            st.session_state.username = ""
            st.session_state.game_stage = 0
            st.session_state.score = 0
            st.rerun()
