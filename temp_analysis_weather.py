"""
Australian Weather Data Analysis System
Developed by: Darshan V Meti
Date: 23/04/2025
Purpose: Analyze multi-year temperature data from Australian weather stations
"""

import os
import pandas as pd
from datetime import datetime

class TemperatureAnalyzer:
    """Core class for processing and analyzing temperature data"""
    
    SEASON_MAP = {
        12: 'Summer', 1: 'Summer', 2: 'Summer',
        3: 'Autumn', 4: 'Autumn', 5: 'Autumn',
        6: 'Winter', 7: 'Winter', 8: 'Winter',
        9: 'Spring', 10: 'Spring', 11: 'Spring'
    }

    def __init__(self, data_folder='temperatures'):
        """Initialize with data folder path"""
        self.data_folder = data_folder
        self.output_folder = 'analysis_results'
        self.data = None

    def _validate_data_file(self, filepath):
        """Validate the structure of a data file"""
        try:
            sample = pd.read_csv(filepath, nrows=1)
            required = {'station_id', 'temperature'}
            if not required.issubset(sample.columns):
                missing = required - set(sample.columns)
                raise ValueError(f"Missing columns: {missing}")
            return True
        except Exception as e:
            print(f"Validation failed for {filepath}: {str(e)}")
            return False

    def load_data(self):
        """Load and combine data from all valid CSV files"""
        if not os.path.exists(self.data_folder):
            raise FileNotFoundError(f"Data folder '{self.data_folder}' not found")

        all_data = []
        for filename in os.listdir(self.data_folder):
            if filename.endswith('.csv'):
                filepath = os.path.join(self.data_folder, filename)
                if self._validate_data_file(filepath):
                    try:
                        year_data = pd.read_csv(filepath)
                        year_data['source_file'] = filename
                        all_data.append(year_data)
                    except Exception as e:
                        print(f"Error loading {filename}: {str(e)}")
        
        if not all_data:
            raise ValueError("No valid data files found")
        
        self.data = pd.concat(all_data, ignore_index=True)
        self._process_data()

    def _process_data(self):
        """Clean and prepare the loaded data"""
        # Convert temperature to numeric
        self.data['temperature'] = pd.to_numeric(
            self.data['temperature'], errors='coerce')
        
        # Handle date information
        if 'date' in self.data.columns:
            self.data['date'] = pd.to_datetime(
                self.data['date'], errors='coerce')
            self.data['month'] = self.data['date'].dt.month
            self.data['year'] = self.data['date'].dt.year
        
        # Remove invalid records
        self.data = self.data.dropna(subset=['station_id', 'temperature'])

    def calculate_seasonal_averages(self):
        """Compute seasonal temperature averages"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        self.data['season'] = self.data['month'].map(self.SEASON_MAP)
        return self.data.groupby('season')['temperature'].mean().round(2)

    def find_extreme_stations(self):
        """Identify stations with largest range and temperature extremes"""
        if self.data is None:
            raise ValueError("No data loaded")
        
        # Calculate station statistics
        stats = self.data.groupby('station_id')['temperature'].agg(
            ['min', 'max', 'mean'])
        stats['range'] = stats['max'] - stats['min']
        
        # Find stations with largest range
        max_range = stats['range'].max()
        max_range_stations = stats[stats['range'] == max_range].index.tolist()
        
        # Find warmest and coolest stations
        warmest = stats['mean'].max()
        warmest_stations = stats[stats['mean'] == warmest].index.tolist()
        
        coolest = stats['mean'].min()
        coolest_stations = stats[stats['mean'] == coolest].index.tolist()
        
        return {
            'max_range': (max_range, max_range_stations),
            'warmest': (warmest, warmest_stations),
            'coolest': (coolest, coolest_stations)
        }

    def save_results(self, seasonal_avgs, extremes):
        """Save all analysis results to files"""
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Save seasonal averages
        with open(f'{self.output_folder}/average_temp.txt', 'w') as f:
            f.write("Seasonal Average Temperatures (°C)\n")
            f.write("================================\n")
            for season, temp in seasonal_avgs.items():
                f.write(f"{season}: {temp:.2f}\n")
        
        # Save temperature range results
        max_range, range_stations = extremes['max_range']
        with open(f'{self.output_folder}/largest_temp_range_station.txt', 'w') as f:
            f.write(f"Maximum Temperature Range: {max_range:.2f}°C\n")
            f.write("Stations with this range:\n")
            for station in range_stations:
                f.write(f"- {station}\n")
        
        # Save temperature extremes
        warm_temp, warm_stations = extremes['warmest']
        cool_temp, cool_stations = extremes['coolest']
        with open(f'{self.output_folder}/warmest_and_coolest_station.txt', 'w') as f:
            f.write("Warmest Stations:\n")
            f.write(f"Average Temperature: {warm_temp:.2f}°C\n")
            for station in warm_stations:
                f.write(f"- {station}\n")
            
            f.write("\nCoolest Stations:\n")
            f.write(f"Average Temperature: {cool_temp:.2f}°C\n")
            for station in cool_stations:
                f.write(f"- {station}\n")

    def run_analysis(self):
        """Execute complete analysis workflow"""
        print("Starting Australian temperature data analysis...")
        
        try:
            # Load and process data
            print("Loading data files...")
            self.load_data()
            print(f"Loaded {len(self.data)} records from {self.data['station_id'].nunique()} stations")
            
            # Perform analyses
            print("Calculating seasonal averages...")
            seasonal_avgs = self.calculate_seasonal_averages()
            
            print("Identifying extreme stations...")
            extremes = self.find_extreme_stations()
            
            # Save results
            print("Saving results...")
            self.save_results(seasonal_avgs, extremes)
            
            print(f"\nAnalysis complete! Results saved to '{self.output_folder}' folder")
            
        except Exception as e:
            print(f"Analysis failed: {str(e)}")

if __name__ == "__main__":
    analyzer = TemperatureAnalyzer()
    analyzer.run_analysis()