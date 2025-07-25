# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 20:21:31 2025

@author: BSmeaton
"""

import json
import logging
import os
import re
from datetime import datetime

import branca.colormap as cm
import folium
import numpy as np
import pandas as pd
import requests
from folium.plugins import HeatMap

# Configuration
API_URL = "https://api.quickbase.com/v1/records/query"
REALM = "uirtus"  # Replace with your Quickbase realm
TABLE_ID = "buq926ivz"  # Replace with your Quickbase table ID
FIELD_IDS = [19, 22, 23, 114, 26]  # Field IDs to fetch

API_TOKEN = "b8pdtw_qq8q_0_5ikmhkb742wheds46gbureswxu"
if not API_TOKEN:
    raise EnvironmentError("Please set the QUICKBASE_API_TOKEN environment variable.")

HEADERS = {
    "QB-Realm-Hostname": f"{REALM}.quickbase.com",
    "Authorization": f"QB-USER-TOKEN {API_TOKEN}",
    "Content-Type": "application/json",
}


def fetch_records(table_id, field_ids):
    records = []
    has_more = True
    skip = 0
    top = 4000  # Number of records per request

    while has_more:
        payload = {
            "from": table_id,
            "select": field_ids,
            "options": {"skip": skip, "top": top},
        }
        response = requests.post(API_URL, json=payload, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        records.extend(data.get("data", []))
        has_more = data.get("metadata", {}).get("hasMore", False)
        skip += top

    return records


def flatten_dicts(df):
    while True:
        cols = [
            c for c in df.columns if df[c].apply(lambda x: isinstance(x, dict)).any()
        ]
        if not cols:
            break
        for c in cols:
            e = df[c].apply(lambda x: x if isinstance(x, dict) else {}).apply(pd.Series)
            e.columns = [f"{c}_{k}" for k in e.columns]
            df.drop(columns=[c], inplace=True)
            df = pd.concat([df, e], axis=1)
    return df


def records_to_dataframe(records, fields):
    # Create a mapping from field ID to field name
    field_map = {field["id"]: field["label"] for field in fields}

    # Extract data
    data = []
    for record in records:
        row = {}
        for field_id, value in record.items():
            row[field_map.get(int(field_id), field_id)] = value
        data.append(row)

    return pd.DataFrame(data)


def json_to_dataframe(api_json):

    # Check if 'Results' key exists
    if "Results" not in api_json:
        raise KeyError("The JSON data does not contain the 'Results' key.")

    # Extract the list of records
    records = api_json["Results"]

    # Create DataFrame
    df = pd.DataFrame(records)

    # Replace any string 'NaN' with actual NaN values
    df.replace("NaN", np.nan, inplace=True)

    # Convert 'NaN' not in quotes to np.nan (if any)
    df = df.applymap(lambda x: np.nan if isinstance(x, float) and np.isnan(x) else x)

    # Convert date strings to datetime objects
    date_columns = ["date", "Latestdatetime"]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


if __name__ == "__main__":
    response = requests.post(
        API_URL,
        json={"from": TABLE_ID, "select": FIELD_IDS, "options": {"top": 1}},
        headers=HEADERS,
    )
    response.raise_for_status()
    fields = response.json().get("fields", [])

    records = fetch_records(TABLE_ID, FIELD_IDS)
    df = records_to_dataframe(records, fields)
    df_quickbase = flatten_dicts(df)

    url = f"http://52.142.192.63/overwatch/v1/sitedata/?records=99999"
    payload = {}
    headers = {"Authorization": "Basic RFN3b2VuZHdydDpkc25qc2QzNG41NCMybTU0ISFSVA=="}
    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()  # Raises stored HTTPError, if one occurred.

    # Preprocess the JSON string to replace NaN with null
    json_str = response.text.replace("NaN", "null")

    # Parse the corrected JSON string
    api_json = json.loads(json_str)

    # Convert JSON to DataFrame
    df_overwatch = json_to_dataframe(api_json)

    # Clean and prepare the columns for merging
    df_quickbase["Site - Item ID_value"] = (
        df_quickbase["Site - Item ID_value"].astype(str).str.strip().str.upper()
    )
    df_overwatch["HT_SiteID"] = (
        df_overwatch["HT_SiteID"].astype(str).str.strip().str.upper()
    )

    df_combined = pd.merge(
        df_quickbase,
        df_overwatch,
        left_on="Site - Item ID_value",
        right_on="HT_SiteID",
        how="inner",
        suffixes=("_quickbase", "_overwatch"),
    )

    # Optionally, drop the redundant 'HT_SiteID' column
    df_combined.drop("HT_SiteID", axis=1, inplace=True)

    df_combined = df_combined.dropna(
        subset=["Site - Lat (D/M/S)_value", "Site - Long (D/M/S)_value", "Power_uptime"]
    )

    mean_lat = df_combined["Site - Lat (D/M/S)_value"].mean()
    mean_lon = df_combined["Site - Long (D/M/S)_value"].mean()

    m = folium.Map(location=[mean_lat, mean_lon], zoom_start=6)

    uptime_min = df_combined["Power_uptime"].min()
    uptime_max = df_combined["Power_uptime"].max()

    # A) For HeatMap plugin
    gradient = {"0.0": "blue", "0.5": "yellow", "1.0": "red"}

    # B) For legend display
    colormap = cm.LinearColormap(
        colors=["blue", "yellow", "red"], vmin=uptime_min, vmax=uptime_max
    )
    colormap.caption = "Power Uptime"
    colormap.add_to(m)

    # ----------------------------------------
    # 4. Add HeatMap Layer
    # ----------------------------------------
    heat_data = df_combined[
        ["Site - Lat (D/M/S)_value", "Site - Long (D/M/S)_value", "Power_uptime"]
    ].values.tolist()

    HeatMap(
        heat_data,
        name="Power Uptime Heatmap",
        gradient=gradient,
        min_value=uptime_min,
        max_value=uptime_max,
        radius=20,
        blur=15,
        max_zoom=1,
    ).add_to(m)

    # (Optional) Add a layer control if you have multiple layers
    folium.LayerControl().add_to(m)

    # ----------------------------------------
    # 5. Save or Show
    # ----------------------------------------
    m.save("power_uptime_heatmap_with_legend.html")
    print("Map saved to power_uptime_heatmap_with_legend.html")
