
import pandas as pd
import requests
import matplotlib.pyplot as plt

url = "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/cambornedata.txt"

response = requests.get(url)
file_contents = response.text

data_lines = file_contents.splitlines()[7:]

data_rows = []
for line in data_lines:
    values = line.split()
    if len(values) == 7:
        values = [value.replace('#', '') for value in values]
        data_rows.append(values)

df = pd.DataFrame(data_rows, columns=["Year", "Month", "Max Temp", "Min Temp", "Air Frost Days", "Rainfall (mm)", "Sunshine Hours"])

numeric_columns = ["Year", "Month", "Max Temp", "Min Temp", "Air Frost Days", "Rainfall (mm)", "Sunshine Hours"]
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors="coerce")

mean_by_year = df.groupby("Year").mean()

monthly_averages = df.groupby("Month").mean()

fig, ax = plt.subplots()

variables = ["Max Temp", "Min Temp", "Air Frost Days", "Rainfall (mm)", "Sunshine Hours"]

for variable in variables:
    ax.plot(monthly_averages.index, monthly_averages[variable], label=variable)

ax.set_xlabel("Month")
ax.set_ylabel("Value")
ax.set_title("Monthly Averages")

ax.legend()

plt.tight_layout()
plt.show()