import matplotlib.pyplot as plt
import pandas as pd

# Step 1 & 2: Create a DataFrame for the last 24 hours of consumption
consumption_data = [
    2.42,
    2.48,
    2.51,
    2.47,
    2.44,
    2.50,
    2.53,
    2.45,
    2.49,
    2.52,
    2.46,
    2.50,
    2.43,
    2.55,
    5.82,
    2.48,
    2.51,
    2.47,
    2.49,
    2.53,
    2.46,
    2.44,
    2.50,
    2.49,
]
hours = list(range(24))
df = pd.DataFrame({"Hour": hours, "Fuel_Consumption_L": consumption_data})

# Step 3: Plot the line chart with markers
plt.figure(figsize=(12, 6))
plt.plot(
    df["Hour"],
    df["Fuel_Consumption_L"],
    marker="o",
    linestyle="-",
    color="blue",
    label="Consumption (L)",
)

# Highlight potential anomaly
anomaly_hour = df["Fuel_Consumption_L"].idxmax()
plt.plot(
    df["Hour"][anomaly_hour],
    df["Fuel_Consumption_L"][anomaly_hour],
    "ro",
    label="Possible Anomaly",
)

# Labels and title
plt.title("Hourly Fuel Consumption (Last 24 Hours)")
plt.xlabel("Hour of Day")
plt.ylabel("Fuel Consumption (Liters)")
plt.xticks(range(24))
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
