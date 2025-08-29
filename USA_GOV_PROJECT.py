#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analysis of 2012 Bitly/USA.gov click data to understand user demographics,
specifically time zones and operating systems used to access government links.
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Data Ingestion
print("Loading JSON data...")
data_file = "data/usagov_bitly_data2012-03-16-1331923249-checkpoint.txt"

# Parse each line of the file into a list of Python dictionaries
records = [json.loads(line) for line in open(data_file)]

# Convert the list of records into a structured DataFrame
df = pd.DataFrame(records)
print(f"DataFrame loaded successfully. Shape: {df.shape}")
print("\nSample data:")
print(df.head())

# 2. Time Zone Analysis
print("\n" + "=" * 50)
print("TIME ZONE ANALYSIS")
print("=" * 50)

# Extract the time zone column
time_zones = df["tz"]

# Handle missing data: fill NaN and empty strings
time_zones_clean = time_zones.fillna("Missing")
time_zones_clean = time_zones_clean.replace("", "Unknown")

# Count the frequency of each time zone
tz_frequency = time_zones_clean.value_counts()
print("Top 10 most frequent time zones:")
print(tz_frequency.head(10))

# Visualize the top time zones
top_10_tz = tz_frequency.head(10)
top_10_tz.plot(kind="barh", title="Top 10 User Time Zones", color="teal")
plt.xlabel("Number of Users")
plt.tight_layout()
plt.show()

# 3. User Agent (Browser/OS) Analysis
print("\n" + "=" * 50)
print("USER AGENT ANALYSIS")
print("=" * 50)

# Remove missing user-agent entries and extract the first token (often the browser/application name)
user_agents = df["a"].dropna()
primary_agent = user_agents.apply(lambda agent: agent.split()[0])
print("Top 10 most common primary agents:")
print(primary_agent.value_counts().head(10))

# 4. Operating System Detection
print("\n" + "=" * 50)
print("OPERATING SYSTEM ANALYSIS")
print("=" * 50)

# Create a working copy of the DataFrame with no missing user-agent strings
df_clean = df[df["a"].notna()].copy()

# Classify users into Windows vs. Non-Windows based on the user-agent string
df_clean["operating_system"] = np.where(
    df_clean["a"].str.contains(
        "Windows", case=False
    ),  # Condition: if 'Windows' is found
    "Windows",  # Value if True
    "Not Windows",  # Value if False
)

print("Operating System Distribution:")
print(df_clean["operating_system"].value_counts())

# 5. Cross-Analysis: Time Zone vs. Operating System
print("\n" + "=" * 50)
print("TIME ZONE AND OS CROSS-ANALYSIS")
print("=" * 50)

# Group data by time zone and OS, then count the number in each group
grouped_data = df_clean.groupby(["tz", "operating_system"]).size()

# Reshape the data to have OS as columns
os_by_tz = grouped_data.unstack().fillna(0)

# Calculate total users per time zone and get the indices of the top 10
top_tz_indices = os_by_tz.sum(axis=1).nlargest(10).index

# Filter the DataFrame to only include the top 10 time zones
top_os_by_tz = os_by_tz.loc[top_tz_indices]

print("Top 10 Time Zones with OS breakdown:")
print(top_os_by_tz)

# Plot the absolute counts
top_os_by_tz.plot(
    kind="barh", stacked=True, title="Top 10 Time Zones by Operating System"
)
plt.xlabel("Number of Users")
plt.tight_layout()
plt.show()

# Plot the normalized proportions for a fair comparison
proportions = top_os_by_tz.div(top_os_by_tz.sum(axis=1), axis=0)
proportions.plot(
    kind="barh", stacked=True, title="Top 10 Time Zones by OS (Normalized Proportions)"
)
plt.xlabel("Proportion of Users")
plt.tight_layout()
plt.show()

print("\nAnalysis complete!")
