import matplotlib.pyplot as plt
import pandas as pd

# 1. Create a DataFrame for the last 24 hours of consumption
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

df = pd.DataFrame({"hour": range(24), "consumption": consumption_data})

# 3. Plot a line chart
plt.figure(figsize=(10, 5))
plt.plot(df["hour"], df["consumption"], marker="o", linestyle="-", color="blue")
plt.title("Hourly Fuel Consumption")
plt.xlabel("Hour")
plt.ylabel("Consumption (liters)")
plt.grid(True)
plt.tight_layout()

# 4. Highlight the potential anomaly
anomaly_hour = df.loc[df["consumption"].idxmax(), "hour"]
anomaly_value = df["consumption"].max()
plt.scatter(anomaly_hour, anomaly_value, color="red", s=100, label="Possible anomaly")
plt.legend()

# Show the plot
plt.show()
