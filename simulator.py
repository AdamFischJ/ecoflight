import math
import pandas as pd

def simulate_dispersion(wind_data):
    """
    Simulates the dispersion of a wind-carried material over time using wind data.

    Parameters:
        wind_data (pd.DataFrame): DataFrame with columns 'lat', 'lon',
                                  'wind_speed_mps', and 'wind_direction_deg'

    Returns:
        list of (lat, lon) tuples representing the simulated path
    """
    KM_PER_DEG_LAT = 111  # Approximate km per degree latitude

    # Use starting point from the first row of wind data
    start_lat = wind_data['lat'].iloc[0]
    start_lon = wind_data['lon'].iloc[0]

    positions = [(start_lat, start_lon)]
    current_lat = start_lat
    current_lon = start_lon

    for _, row in wind_data.iterrows():
        speed_kmph = row['wind_speed_mps'] * 3.6  # convert m/s to km/h
        angle_rad = math.radians(row['wind_direction_deg'])

        delta_lat = (speed_kmph * math.cos(angle_rad)) / KM_PER_DEG_LAT
        delta_lon = (speed_kmph * math.sin(angle_rad)) / (
            KM_PER_DEG_LAT * math.cos(math.radians(current_lat))
        )

        current_lat += delta_lat
        current_lon += delta_lon
        positions.append((current_lat, current_lon))

    return positions