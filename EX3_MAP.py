# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 12:23:01 2025

@author: BSmeaton
"""
import folium
import pandas as pd


def main():
    capacity_threshold = 500  # Threshold for Structure Capacity (Existing)

    # Read the CSV file with headers
    df = pd.read_csv("TZ_Data.csv")

    # Convert relevant columns to numeric
    df["Structure Capacity (Existing)"] = pd.to_numeric(
        df["Structure Capacity (Existing)"], errors="coerce"
    )
    df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
    df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

    # Filter rows
    df_filtered = df[df["Structure Capacity (Existing)"] > capacity_threshold]

    # Extract latitudes and longitudes
    latitudes = df_filtered["Latitude"]
    longitudes = df_filtered["Longitude"]

    # Calculate map center
    center_lat = latitudes.mean()
    center_lon = longitudes.mean()

    # Create the map
    my_map = folium.Map(location=[center_lat, center_lon], zoom_start=2)

    # Add markers
    for lat, lon in zip(latitudes, longitudes):
        if pd.notna(lat) and pd.notna(lon):
            folium.Marker(location=[lat, lon]).add_to(my_map)

    # Save the map
    my_map.save("output_map.html")
    print("Map saved to 'output_map.html'.")


if __name__ == "__main__":
    main()
