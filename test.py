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
        st.title("🌐 Game 2: Map the Power Outliers")

        st.markdown(
            """
            One of your regional managers at Helios just called:

            > _“We think some sites have **unusual power uptime** — maybe they're running too well... or too poorly. Can you show us the hotspots on a map?”_

            🚧 Your mission is to visualize this across all sites using two real APIs:
            - The **Quickbase** site info database
            - The **Overwatch** power metrics API

            You'll combine both datasets and **build a heatmap** showing power uptime intensity across sites.

            ---
            🧠 **Copy this prompt into ChatGPT exactly as shown below to generate the working Python code:**
            ```python
            Write Python code that:

            1. Calls the Quickbase API using:
                - URL: https://api.quickbase.com/v1/records/query
                - Realm: "uirtus"
                - Table ID: "buq926ivz"
                - Field IDs: [19, 22, 23, 114, 26]
                - Token: "b8pdtw_qq8q_0_5ikmhkb742wheds46gbureswxu"

            2. Fetches additional site data from:
                - URL: http://52.142.192.63/overwatch/v1/sitedata/?records=99999
                - Headers: {"Authorization": "Basic RFN3b2VuZHdydDpkc25qc2QzNG41NCMybTU0ISFSVA=="}

            3. Processes and cleans both datasets:
                - Replaces string 'NaN' with np.nan
                - Converts date columns to datetime
                - Flattens nested Quickbase fields
                - Merges datasets on site ID
                - Keeps rows with latitude, longitude, and power uptime

            4. Plots a **folium heatmap** of `Power_uptime` using:
                - Lat: "Site - Lat (D/M/S)_value"
                - Lon: "Site - Long (D/M/S)_value"
                - Value: "Power_uptime"
                - Color scale: blue → yellow → red

            5. Adds a legend (LinearColormap) for power uptime

            6. Saves the map as `power_uptime_heatmap_with_legend.html`

            The output must include the full working script, using:
            - pandas, numpy, requests, folium, branca.colormap, and folium.plugins.HeatMap
            - No simplification — give me the exact production-level code for this task
            ```

            ---
            🔍 When you run the code in your local Python environment, it will generate a heatmap showing which Helios sites have the **lowest and highest power uptime**. Those red zones? You might want to check them out.

            ✅ Once you’ve created your map, hit **Finish** to continue.
            """
        )

        if st.button("Finish Game 2"):
            st.session_state.score += 1
            st.session_state.game_stage += 1
            st.balloons()
            st.rerun()

    # === GAME 3 ===
    elif st.session_state.game_stage == 2:
        st.header("🏙️ Game 3: Rent Race — Prompt Your Way to the Top")
        # st.image("https://i.imgur.com/N2dztxz.png", width=400)

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
        # st.image("https://i.imgur.com/xuwKQ6y.jpeg", width=400)

        st.markdown(
            """
            Let’s visualize your dream tower in 3D with alternating red and white segments.

            🧱 Your tower will be built using stacked 10m-high cylinders.

            ---
            📋 **Copy this prompt into ChatGPT:**
            ```python
            Use Plotly in Python to create a 3D tower with 6 stacked cylinders.
            - Each cylinder is 10 meters high
            - Alternate red and white colors
            - Use go.Cylinder or go.Mesh3d if available
            - Label each segment with its height level
            - Make it look cool!
            ```

            ---
            🔍 This is your final creative mission — no right or wrong answers, just fun with Python and visualization!
            """
        )

        if st.button("Finish Game 4"):
            st.session_state.score += 1
            st.session_state.game_stage += 1
            st.balloons()
            st.rerun()
