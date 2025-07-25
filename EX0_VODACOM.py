import matplotlib.pyplot as plt
import pandas as pd

# Create dummy data similar to your Excel structure
data = {
    "HT ID": ["MGKN0003", "MGKN0004", "MGKN0005", "MGKN0006", "MGKN0007", "MGKN0008"],
    "Customer ID": ["", "", "", "", "", ""],
    "Site Name": ["Kingatoko", "Pdg Commerce", "Matadi", "Lukala", "Boma", "Muanda"],
    "Finance ID": [10067, 10071, 10072, 10073, 10074, 10075],
    "Region": [
        "Bas-Congo",
        "Kinshasa",
        "Bas-Congo",
        "Bas-Congo",
        "Kinshasa",
        "Equateur",
    ],
    "Location": ["R1", "R1", "R2", "R2", "R1", "R3"],
    "Category": ["Colocation"] * 6,
    "Tenancy Type": ["Ex-Tigo", "Ex-Tigo", "Vodacom", "Vodacom", "Vodacom", "Ex-Tigo"],
    "Grid": ["Off Grid", "Grid", "Grid", "Off Grid", "Grid", "Off Grid"],
    "Multi-Tenant": ["Multi Tenant"] * 6,
    "Tenancy Class": [
        "Ex-Tigo Colocation Off Grid",
        "Ex-Tigo Colocation Grid",
        "Vodacom Grid",
        "Vodacom Off Grid",
        "Vodacom Grid",
        "Ex-Tigo Off Grid",
    ],
    "UCSAF?": [""] * 6,
    "Lease Start Date": pd.to_datetime(
        [
            "2015-07-13",
            "2015-02-26",
            "2016-03-15",
            "2017-06-01",
            "2018-09-12",
            "2019-11-20",
        ]
    ),
    "Multi-Tenant Date": [pd.NaT] * 6,
    "Invoice Date": pd.to_datetime(
        [
            "2015-07-13",
            "2015-02-26",
            "2016-03-15",
            "2017-06-01",
            "2018-09-12",
            "2019-11-20",
        ]
    ),
    "Lease Rate": [3500, 3500, 4200, 3900, 4400, 3600],
    "Currency": ["USD"] * 6,
}

# Load into a DataFrame
df = pd.DataFrame(data)

# Group by 'Region' and calculate average 'Lease Rate'
average_lease_rate = df.groupby("Region")["Lease Rate"].mean().reset_index()

# Sort by lease rate
average_lease_rate = average_lease_rate.sort_values(by="Lease Rate", ascending=False)

# Plot
plt.figure(figsize=(10, 6))
plt.bar(average_lease_rate["Region"], average_lease_rate["Lease Rate"], color="skyblue")
plt.title("Average Lease Rate by Region", fontsize=16)
plt.xlabel("Region", fontsize=14)
plt.ylabel("Average Lease Rate (USD)", fontsize=14)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
