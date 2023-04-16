import pandas as pd
import numpy as np
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = (np.sin(dlat / 2) * np.sin(dlat / 2) +
         np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) *
         np.sin(dlon / 2) * np.sin(dlon / 2))
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return R * c

# Load datasets
aircraft_types = pd.read_csv('aircraft_type.csv')
airports = pd.read_csv('airport.csv')
flight_scenarios = pd.read_csv('flight_scenarios.csv')

# Create a dictionary to map aerodromes to airports and their coordinates
aerodrome_to_airport = {}
for index, row in airports.iterrows():
    aerodrome_to_airport[row['airport_icao']] = {'airport_name': row['airport_name'],
                                                 'latitude': row['latitude'],
                                                 'longitude': row['longitude']}

# Compute CO2 emissions for each scenario
for index, row in flight_scenarios.iterrows():
    # Map aerodromes to airports and get their coordinates
    departure_coords = (aerodrome_to_airport[row['departure_aerodrome']]['latitude'],
                        aerodrome_to_airport[row['departure_aerodrome']]['longitude'])
    destination_coords = (aerodrome_to_airport[row['destination_aerodrome']]['latitude'],
                          aerodrome_to_airport[row['destination_aerodrome']]['longitude'])

    # Calculate distance between the departure and destination airports
    distance = haversine(*departure_coords, *destination_coords)

    # Compute CO2 emissions
    co2_emission = distance * 0.2  # Replace 0.2 with the appropriate specific_fuel_consumption value for the given aircraft type

    print(f"Scenario {row['scenario_id']} - CO2 emission: {co2_emission} kg")
