import math
import pandas as pd

def simulate_dispersion(wind_data, material_type="smoke"):
    """
    Simulates wind-driven material spread using basic physics adjustments based on material type.
    Returns the path as a list of (lat, lon), the total distance traveled, and max wind speed.
    """

    # Material-based physics adjustments
    if material_type == "pollen":
        drag_coefficient = 0.85
        speed_multiplier = 0.6
    elif material_type == "plastic":
        drag_coefficient = 1.1
        speed_multiplier = 0.9
    else:  # smoke or default
        drag_coefficient = 0.7
        speed_multiplier = 0.3

    KM_PER_DEG_LAT = 111  # Rough km per degree latitude
    start_lat = wind_data['lat'].iloc[0]
    start_lon = wind_data['lon'].iloc[0]

    positions = [(start_lat, start_lon)]
    current_lat = start_lat
    current_lon = start_lon
    total_distance = 0.0
    max_wind = 0.0

    for _, row in wind_data.iterrows():
        # Convert wind speed (m/s) to km/h and scale by material
        wind_speed_kmph = row['wind_speed_mps'] * 3.6 * speed_multiplier
        wind_dir_deg = row['wind_direction_deg']
        angle_rad = math.radians(wind_dir_deg)

        # Max wind tracking
        if row['wind_speed_mps'] > max_wind:
            max_wind = row['wind_speed_mps']

        # Distance in km moved along latitude and longitude
        delta_lat = (wind_speed_kmph * math.cos(angle_rad)) / KM_PER_DEG_LAT
        delta_lon = (wind_speed_kmph * math.sin(angle_rad)) / (KM_PER_DEG_LAT * math.cos(math.radians(current_lat)))

        current_lat += delta_lat
        current_lon += delta_lon
        positions.append((current_lat, current_lon))

        total_distance += math.sqrt(delta_lat**2 + delta_lon**2) * KM_PER_DEG_LAT

    return positions, round(total_distance, 2), round(max_wind, 2)
