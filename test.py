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
        st.experimental_rerun()

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
                st.experimental_rerun()
            else:
                st.error("Hmm, not quite. Look at that spike again!")

    # === GAME 2 ===
    elif st.session_state.game_stage == 1:
        st.header("🛰️ Game 2: Help an FE find the tallest tower")
        st.image("https://i.imgur.com/zB4nFsn.png", width=400)

        st.markdown(
            """
        A field engineer just landed in Tanzania, and their first task is to climb the **tallest tower** in the region.

        🔍 Use the Quickbase API and ChatGPT to find the site with the tallest tower.

        **Copy and paste this prompt into ChatGPT:**
        ```
        Use the Quickbase API to find the site with the tallest tower.
        API: https://api.quickbase.com/v1/records/query
        Token: b8pdtw_qq8q_0_5ikmhkb742wheds46gbureswxu
        Table ID: buq926ivz
        Realm: uirtus
        Fields: Site ID (19), Tower Height (114)

        Return the site ID of the tallest tower.
        ```
        """
        )

        answer = (
            st.text_input("Enter the Site ID of the tallest tower:").strip().upper()
        )
        if st.button("Submit Game 2"):
            if answer == correct_answers[1]:
                st.success("Correct! The FE has packed their climbing gear. 🧗‍♂️")
                st.balloons()
                st.session_state.score += 1
                st.session_state.game_stage += 1
                st.experimental_rerun()
            else:
                st.error("Hmm, that’s not the tallest. Try again!")

    # === GAME 3 ===
    elif st.session_state.game_stage == 2:
        st.header("🌍 Game 3: Map the Strong Towers")
        st.image("https://i.imgur.com/KGHshtj.jpeg", width=400)

        st.markdown(
            """
        We only want to visit towers with a strong structure!

        🧠 Use the Quickbase API to pull towers with **structure capacity > 500** and plot them using `folium`.

        **Copy and paste this into ChatGPT:**
        ```
        Use Quickbase API to fetch tower sites with lat/lon and structure capacity > 500.
        API: https://api.quickbase.com/v1/records/query
        Token: b8pdtw_qq8q_0_5ikmhkb742wheds46gbureswxu
        Table ID: buq926ivz
        Fields: Latitude (22), Longitude (23), Structure Capacity (26)

        Plot these towers on a folium map and count how many appear.
        ```
        """
        )

        answer = st.text_input("How many towers were shown on your map?")
        if st.button("Submit Game 3"):
            if answer == correct_answers[2]:
                st.success("That’s right! You’ve mapped the strongest towers. 🗺️")
                st.session_state.score += 1
                st.session_state.game_stage += 1
                st.experimental_rerun()
            else:
                st.error("Hmm, that count doesn’t match. Try again!")

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
                st.experimental_rerun()
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
            st.experimental_rerun()
