"""
Question 2 - Weather data analysis 
# This program analyses the temperature data stored in CSV files, 
# calculate the requested statistics, 
# and save the results to the specified text files.


# Instructions for this program:
# - Place the temperature_data folder in the same directory as this python script.
# - Place empty files named "average_temp.txt", "largest_temp_range_station.txt"
#    and "warmest_and_coolest_station.txt in the same directory as this python script.
# - Install pandas if not already installed using pip install pandas.
"""

import os
import pandas as pd

# Define paths

SCRIPT_FILE= __file__
DIR_FILE = os.path.dirname(os.path.abspath(SCRIPT_FILE))

TEMPERATURES_FOLDERNAME = 'temperature_data'
AVERAGE_TEMP_FILENAME= "average_temp.txt"
LARGEST_TEMP_RANGE_FILENAME = "largest_temp_range_station.txt"
WARMEST_AND_COOLEST_FILENAME = "warmest_and_coolest_station.txt"

TEMPERATURES_FOLDER = DIR_FILE + "/" + TEMPERATURES_FOLDERNAME
AVERAGE_TEMP_FILE = DIR_FILE + "/" + AVERAGE_TEMP_FILENAME
LARGEST_TEMP_RANGE_FILE = DIR_FILE + "/" + LARGEST_TEMP_RANGE_FILENAME
WARMEST_AND_COOLEST_FILE = DIR_FILE + "/" + WARMEST_AND_COOLEST_FILENAME

# Define season mapping
SEASON_MAP = {
    "Summer": ["December", "January", "February"],
    "Autumn": ["March", "April", "May"],
    "Winter": ["June", "July", "August"],
    "Spring": ["September", "October", "November"],
}


def checkfiles():
    if not os.path.exists(TEMPERATURES_FOLDER) or not os.path.isfile(AVERAGE_TEMP_FILE) or not os.path.isfile(LARGEST_TEMP_RANGE_FILE) or not os.path.isfile(WARMEST_AND_COOLEST_FILE) :
     # End the function if the file does not exist
            return False

    return True

def process_temperature_data():
    # Data containers

    seasonal_temps = {season: [] for season in SEASON_MAP.keys()}
    station_temps = {}

    # Process all CSV files in the folder
    for file_name in os.listdir(TEMPERATURES_FOLDER):
        if file_name.endswith(".csv"):
            file_path = os.path.join(TEMPERATURES_FOLDER, file_name)
            data = pd.read_csv(file_path)

            # Ensure necessary columns exist
            if not {"STATION_NAME", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"}.issubset(data.columns):
                continue

            # Iterate through the rows
            for _, row in data.iterrows():
                station = row["STATION_NAME"]

                # Aggregate temperatures by season
                for season, months in SEASON_MAP.items():
                    temps = [row[month] for month in months if pd.notnull(row[month])]
                    seasonal_temps[season].extend(temps)

                # Collect all temperatures for each station
                if station not in station_temps:
                    station_temps[station] = []
                station_temps[station].extend(
                    [row[month] for month in data.columns[4:] if pd.notnull(row[month])]
                )

    # Task 1: Calculate average temperatures for each season
    average_seasonal_temps = {
        season: (sum(temps) / len(temps)) if temps else 0.0
        for season, temps in seasonal_temps.items()
    }
    with open(AVERAGE_TEMP_FILE, "w") as file:
        file.write("Average Temperatures by Season:\n")
        for season, avg_temp in average_seasonal_temps.items():
            file.write(f"{season}: {avg_temp:.2f}°C\n")

    # Task 2: Find station(s) with the largest temperature range
    temp_ranges = {
        station: max(temps) - min(temps) if temps else 0.0
        for station, temps in station_temps.items()
    }
    max_range = max(temp_ranges.values())
    largest_range_stations = [
        station for station, range_ in temp_ranges.items() if range_ == max_range
    ]
    with open(LARGEST_TEMP_RANGE_FILE, "w") as file:
        file.write("Station(s) with Largest Temperature Range:\n")
        for station in largest_range_stations:
            file.write(f"{station}: {max_range:.2f}°C\n")

    # Task 3: Find warmest and coolest stations (using actual temperature extremes)
    warmest_stations = []
    coolest_stations = []
    max_temp = float('-inf')
    min_temp = float('inf')

    for station, temps in station_temps.items():
        if temps:
            station_max = max(temps)
            station_min = min(temps)
            if station_max > max_temp:
                max_temp = station_max
                warmest_stations = [station]
            elif station_max == max_temp:
                warmest_stations.append(station)
            if station_min < min_temp:
                min_temp = station_min
                coolest_stations = [station]
            elif station_min == min_temp:
                coolest_stations.append(station)

    with open(WARMEST_AND_COOLEST_FILE, "w") as file:
        file.write("Warmest Station(s):\n")
        for station in warmest_stations:
            file.write(f"{station}: {max_temp:.2f}°C\n")
        file.write("\nCoolest Station(s):\n")
        for station in coolest_stations:
            file.write(f"{station}: {min_temp:.2f}°C\n")

    print("Analysis complete. Results written to files.")

# Run the analysis
file_checked=checkfiles()

if file_checked == True:
    process_temperature_data()
else:
    print("Files missing.  Please read instructions")
