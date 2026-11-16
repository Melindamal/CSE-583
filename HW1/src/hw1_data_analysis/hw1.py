import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("bicycle_data.csv")

# Columns in the dataframe:
#   Date: timestamp marking the hour in which bicycles were counted
#         (e.g. "10/02/2012 01:00:00 PM"). Should be datetime64. Pandas
#         loads it as a string (object), so I convert it with pd.to_datetime.
#   Fremont Bridge Sidewalks, south of N 34th St Total: total bicycles
#         crossing the bridge that hour (east + west sidewalks). Should be
#         numeric. float64 is correct because the column has missing values
#         (NaN), which a plain int64 cannot hold.
#   Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk:
#         bicycles counted on the west sidewalk that hour. Should be numeric
#         (float64, same reason as above).
#   Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk:
#         bicycles counted on the east sidewalk that hour. Should be numeric
#         (float64, same reason as above).

df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y %I:%M:%S %p")
df = df.rename(columns={
    "Fremont Bridge Sidewalks, south of N 34th St Total": "Total_given",
    "Fremont Bridge Sidewalks, south of N 34th St Cyclist West Sidewalk": "West",
    "Fremont Bridge Sidewalks, south of N 34th St Cyclist East Sidewalk": "East",
})
#print(df.dtypes)

# Total bicycle count = East + West sidewalk counts.
# If either side is missing (NaN), the total is NaN as well.
df["Total"] = df["East"] + df["West"]

# Hour of the day (0-23), taken from the datetime Date column.
df["Hour"] = df["Date"].dt.hour

# Year, taken from the datetime Date column.
df["Year"] = df["Date"].dt.year

# New dataframe containing only the rows from the year 2016.
df_2016 = df[df["Year"] == 2016].copy()

# Missing data: 1 time point in 2016 has missing data (2016-03-13 02:00:00).
# East, West, and Total are all NaN for that hour. This is the daylight
# saving time "spring forward" hour, which doesn't exist on that date.
n_missing = df_2016["Total"].isna().sum()
print("Time points with missing data:", n_missing)

# Dropped the row with missing Total so it cannot affect the hourly
# plot or the busiest-hour calculation.
df_2016 = df_2016.dropna(subset=["Total"])

# Average total bicycle count for each hour of the day (0-23) in 2016.
by_hour = df_2016.groupby("Hour")["Total"].mean()

ax = by_hour.plot(kind="line", marker="o")
ax.set_title("Average Fremont Bridge Bicycle Crossings by Hour of Day (2016)")
ax.set_xlabel("Hour of day (0-23)")
ax.set_ylabel("Average bicycles per hour")
ax.set_xticks(range(0, 24, 2))
ax.grid(True, alpha=0.3)

plt.savefig("counts_by_hour.png", dpi=150, bbox_inches="tight")
plt.close()

# Busiest hour of the day on average: the hour (0-23) whose mean Total
# bicycle count across all of 2016 is highest.
busiest_hour = by_hour.idxmax()
busiest_avg = by_hour.max()

print("Busiest hour:", busiest_hour)
print("Average count at that hour:", busiest_avg)

# The busiest hour on average in 2016 is hour 17 (5:00-5:59 PM), with an
# average of about 399 bicycles per hour crossing the Fremont Bridge.
# This is the evening commute peak and matches the highest point in
# counts_by_hour.png.