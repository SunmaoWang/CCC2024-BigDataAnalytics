import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
# Enter year-month-date    Ex. 2024-05-12
# Enter start_hour & end_hour Ex.start_hour: 14:00    end_hour: 17:00
# plot curve to show the change of averageValue for data with "timeSeriesName": "1HR_AV".


# Load the JSON data
file_path = '/Users/shangkaichen/Desktop/Cluster and Cloud Computing/A2 study/env_test.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Initialize an empty list to collect data
data_list = []

# Iterate through the hits and extract the time series data
for hit in data['hits']['hits']:
    site_name = hit['_source']['siteName']
    parameters = hit['_source']['parameters']
    
    for parameter in parameters:
        for time_series in parameter['timeSeriesReadings']:
            for reading in time_series['readings']:
                data_list.append({
                    'siteName': site_name,
                    'parameter': parameter['name'],
                    'timeSeriesName': time_series['timeSeriesName'],
                    'since': reading['since'],
                    'until': reading['until'],
                    'averageValue': reading.get('averageValue')
                })

# Create a DataFrame from the list
df = pd.DataFrame(data_list)

# Convert 'since' and 'until' to datetime and remove timezone information
df['since'] = pd.to_datetime(df['since']).dt.tz_localize(None)
df['until'] = pd.to_datetime(df['until']).dt.tz_localize(None)

# Function to fetch data for a specified date and time range
def fetch_data_for_range(date_str, start_hour, end_hour):
    start_time = datetime.strptime(f'{date_str} {start_hour}', '%Y-%m-%d %H:%M')
    end_time = datetime.strptime(f'{date_str} {end_hour}', '%Y-%m-%d %H:%M')
    
    # Filter the data for the specified time range
    filtered_data = df[(df['since'] >= start_time) & (df['until'] <= end_time)]
    
    return filtered_data

# Function to plot data for a specified date and time range
def plot_data_for_range(date_str, start_hour, end_hour):
    filtered_data = fetch_data_for_range(date_str, start_hour, end_hour)
    
    for site_name in filtered_data['siteName'].unique():
        site_data = filtered_data[filtered_data['siteName'] == site_name]
        plt.figure(figsize=(10, 5))
        for parameter in site_data['parameter'].unique():
            for time_series_name in site_data['timeSeriesName'].unique():
                subset = site_data[(site_data['parameter'] == parameter) & (site_data['timeSeriesName'] == time_series_name)]
                # Sort the subset by the 'since' column to ensure proper time series plotting
                subset = subset.sort_values(by='since')
                plt.plot(subset['since'], subset['averageValue'], marker='o', label=f'{parameter} ({time_series_name})')
        
        plt.title(f'Average Value Time Series for {site_name} on {date_str} from {start_hour} to {end_hour}')
        plt.xlabel('Time')
        plt.ylabel('Average Value')
        plt.legend()
        plt.grid(True)
        plt.show()

# User input for date and time range
date_str = input("Enter date (YYYY-MM-DD): ")
start_hour = input("Enter start hour (HH:MM): ")
end_hour = input("Enter end hour (HH:MM): ")

# Plot the data for the specified date and time range
plot_data_for_range(date_str, start_hour, end_hour)
