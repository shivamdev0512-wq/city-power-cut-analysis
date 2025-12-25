
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ------------------ LOAD DATASET ------------------
FILE_NAME = "city_power_cut_data.csv"

df = pd.read_csv("city_power_cut_data.csv")
print("Dataset loaded successfully.")

# ------------------ DATA CLEANING ------------------
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
df['End_Time'] = pd.to_datetime(df['End_Time'], errors='coerce')
df = df.dropna(subset=['Start_Time', 'End_Time', 'Area'])
df = df[df['End_Time'] > df['Start_Time']]

# ------------------ FEATURE ENGINEERING ------------------
df['Duration_hr'] = (df['End_Time'] - df['Start_Time']).dt.total_seconds() / 3600
df['Date'] = df['Start_Time'].dt.date
df['Month'] = df['Start_Time'].dt.to_period('M')
df['Hour'] = df['Start_Time'].dt.hour

# ------------------ ANALYSIS ------------------
daily_freq = df.groupby('Date').size()
area_freq = df.groupby('Area').size().sort_values(ascending=False)

duration_stats = df.groupby('Area')['Duration_hr'].agg(
    avg_duration='mean',
    max_duration='max',
    total_downtime='sum'
)

# Reliability calculation (assume 30 days month)
TOTAL_PERIOD_HOURS = 24 * 30
reliability = df.groupby('Area')['Duration_hr'].sum().reset_index()
reliability['reliability_%'] = ((TOTAL_PERIOD_HOURS - reliability['Duration_hr']) / TOTAL_PERIOD_HOURS) * 100

# SAIFI & SAIDI
saifi = df.groupby('Area').size() / 30
saidi = df.groupby('Area')['Duration_hr'].sum() / 30

# ------------------ VISUALIZATION ------------------
# Daily frequency plot
plt.figure(figsize=(10,5))
plt.plot(daily_freq.index, daily_freq.values, marker='o')
plt.title("Daily Power Cuts")
plt.xlabel("Date")
plt.ylabel("Number of Cuts")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Area-wise frequency plot
plt.figure(figsize=(8,5))
plt.bar(area_freq.index, area_freq.values, color='orange')
plt.title("Power Cuts by Area")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Boxplot of outage durations by area
plt.figure(figsize=(8,5))
df.boxplot(column='Duration_hr', by='Area')
plt.title("Outage Duration by Area")
plt.suptitle("")
plt.ylabel("Duration (hours)")
plt.tight_layout()
plt.show()

# Reason distribution plot
reason_count = df['reason'].value_counts()
plt.figure(figsize=(8,5))
plt.bar(reason_count.index, reason_count.values, color='green')
plt.title("Power Cut Reasons Distribution")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ------------------ SUMMARY STATISTICS ------------------
print("Duration statistics (hours):")
print(df['Duration_hr'].describe())

print("\nDuration stats per area:")
print(duration_stats)

print("\nReliability per area (%):")
print(reliability)

print("\nSAIFI per area (avg interruptions per day):")
print(saifi)

print("\nSAIDI per area (avg downtime per day):")
print(saidi)