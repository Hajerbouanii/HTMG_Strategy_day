# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 14:27:31 2025

@author: BSmeaton
"""

import matplotlib.pyplot as plt
import pandas as pd
import requests

api_token = "b856uu_qq8q_0_bax7pb6di4dudu2iave5drx5dk"
api_url = "https://api.quickbase.com/v1"
realm = "uirtus"
EQUIPMENT_TABLE_ID = "bukpkaqtr"
field_ids = [3, 7, 12, 15, 18, 33, 106, 184, 185, 186, 187, 193]
# Equipment headings [Record ID#, Status, Tenant, Install Height, Face, Site ID, OpCo2, Equipment Length (mm), Equipment Width (mm), Equipment Depth (mm), Equipment Diameter (mm), Equipment Type]
headers = {
    "QB-Realm-Hostname": f"{realm}.quickbase.com",
    "Authorization": f"QB-USER-TOKEN {api_token}",
    "Content-Type": "application/json",
}

response = requests.post(
    f"{api_url}/records/query",
    verify=False,
    json={
        "from": EQUIPMENT_TABLE_ID,
        "select": field_ids,
        "where": "{33.EX.'TZZA7419'}",
    },
    headers=headers,
).json()

fields = {f["id"]: f["label"] for f in response.get("fields", [])}
df = pd.DataFrame(
    [
        {fields[int(k)]: v.get("value") for k, v in record.items()}
        for record in response.get("data", [])
    ]
)


df["Equipment Type"].fillna("Unknown").value_counts().plot.pie(
    autopct="%1.1f%%", startangle=140, shadow=True, figsize=(8, 8)
)
plt.title("Distribution of Equipment Types")
plt.ylabel("")
plt.axis("equal")
plt.tight_layout()
plt.savefig("equipment_type_distribution_pie_chart.png")
plt.show()
