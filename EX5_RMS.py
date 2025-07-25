# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 14:19:29 2025

@author: BSmeaton
"""

import json

import matplotlib.pyplot as plt
import pandas as pd
import requests

# === CONFIGURATION ===
API_URL = "http://52.142.192.63/rms/rms-power-daily/?records=9999"
AUTH_HEADER = {
    "Authorization": "Basic RFN3b2VuZHdydDpkc25qc2QzNG41NCMybTU0ISFSVA=="  # Update if needed
}

# === FUNCTION TO FETCH & CLEAN DATA ===
# Returned data from data frame takes following headers and format:
# date	site_id	Latestdatetime	load_current_max	load_current_min	load_current_avg	bus_voltage_max	bus_voltage_min	bus_voltage_avg	load_power_max	load_power_min	load_power_avg	Rectifier_current_max	Rectifier_current_min	Rectifier_current_avg	dg_power_max	dg_power_min	dg_power_avg_above0	dg_hours_v1	dg_voltage_1_max	dg_voltage_1_min	dg_voltage_2_max	dg_voltage_2_min	dg_voltage_3_max	dg_voltage_3_min	dg_current_1_max	dg_current_1_min	dg_current_2_max	dg_current_2_min	dg_current_3_max	dg_current_3_min	dg_start_count	battery_current_max	battery_current_min	battery_current_avg	DG_Control_Mode_status	solar_load_max	solar_load_avg	solar_produced	dg_energy_start_of_day	dg_energy_end_of_day
# 2025-04-23 00:00:00	TZMG0844	Wed, 23 Apr 2025 07:53:00 GMT	48.59	38.54	43.405625	51.93	49.47	51.84604167	2.5232787	1.9065738	2.250409842				0	0		0													0	0	-45.93	-0.956875				0	13240.6	13240.6


def fetch_power_data():
    response = requests.get(API_URL, headers=AUTH_HEADER)
    response.raise_for_status()  # Ensure request is successful

    # Replace 'NaN' strings with JSON-compatible nulls
    json_str = response.text.replace("NaN", "null")
    api_json = json.loads(json_str)

    # Extract and convert JSON to DataFrame
    if "Results" not in api_json:
        raise KeyError("The JSON data does not contain the 'Results' key.")

    df = pd.DataFrame(api_json["Results"])

    # Convert date columns to datetime format
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    return df


# === MAIN SCRIPT ===
df = fetch_power_data()
df.to_excel("df.xlsx")

df["dg_energy_consumed"] = df["dg_energy_end_of_day"] - df["dg_energy_start_of_day"]

df["country"] = df["site_id"].str[:2]

country_totals = (
    df.groupby("country", as_index=False)["dg_energy_consumed"]
    .sum()
    .set_index("country")  # index makes the pie labels cleaner
    .squeeze()  # turns the single-column frame into a Series
)

plt.figure()
country_totals.plot(
    kind="pie",
    autopct="%1.1f%%",  # percent labels
    startangle=90,  # optional: rotates the first slice
    ylabel="",  # hides the default y-label
)
plt.title("Total DG Energy Consumption by Country")
plt.tight_layout()
plt.show()
