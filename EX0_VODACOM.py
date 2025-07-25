import matplotlib.pyplot as plt
import pandas as pd

# Define the Excel file and sheet name
EXCEL_FILE = "Vodacom_Rents.xlsx"
SHEET_NAME = "Data"

# HT ID	Customer ID	Site Name	Finance ID	Region	Location	Category	Tenancy Type	Grid	Multi-Tenant	Tenancy Class	UCSAF?	Lease Start Date	Multi-Tenant Date	Invoice Date	Lease Rate	Currency
# DRKN0003		Kingatoko	10067	Bas-Congo	R1	Colocation	Ex-Tigo	Off Grid	Multi Tenant	Ex-Tigo Colocation Off Grid		7/13/2015		7/13/2015	3500	USD
# DRKN0004		Pdg Commerce	10071	Kinshasa	R1	Colocation	Ex-Tigo	Grid	Multi Tenant	Ex-Tigo Colocation Grid		2/26/2015		2/26/2015	3500	USD

# Load the data into a DataFrame
df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)

# Group by 'Region' and calculate the average 'Lease Rate'
average_lease_rate = df.groupby("Region")["Lease Rate"].mean().reset_index()

# Sort the values for better visualization (optional)
average_lease_rate = average_lease_rate.sort_values(by="Lease Rate", ascending=False)

# Create a bar graph
plt.figure(figsize=(10, 6))  # Optional: Adjusts the size of the plot
plt.bar(average_lease_rate["Region"], average_lease_rate["Lease Rate"], color="skyblue")

# Add titles and labels
plt.title("Average Lease Rate by Region", fontsize=16)
plt.xlabel("Region", fontsize=14)
plt.ylabel("Average Lease Rate (USD)", fontsize=14)

# Rotate x-axis labels if there are many regions
plt.xticks(rotation=45, ha="right")

# Adjust layout for better fit
plt.tight_layout()

# Display the plot
plt.show()
