import matplotlib.pyplot as plt
import math
import os

def plot_dispersion(path, output_path="outputs/spread_plot.png"):
    lats, lons = zip(*path)

    plt.figure(figsize=(8, 6))
    plt.plot(lons, lats, marker='o', linestyle='-', color='blue')
    plt.title("Simulated Particle Dispersion Path")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_wind_pattern(wind_data, output_path="outputs/wind_pattern.png"):
    times = wind_data["time"]
    directions = wind_data["wind_direction_deg"]
    speeds = wind_data["wind_speed_mps"]

    fig, ax1 = plt.subplots(figsize=(8, 5))

    ax1.set_title("Wind Direction and Speed (Past 24 Hours)")
    ax1.set_xlabel("Time (UTC)")
    ax1.set_ylabel("Wind Direction (°)", color='tab:blue')
    ax1.plot(times, directions, color='tab:blue', marker='o', label="Direction")
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_ylim(0, 360)

    ax2 = ax1.twinx()
    ax2.set_ylabel("Wind Speed (m/s)", color='tab:red')
    ax2.plot(times, speeds, color='tab:red', linestyle='--', label="Speed")
    ax2.tick_params(axis='y', labelcolor='tab:red')

    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_wind_vector_path(wind_data, output_path="outputs/wind_vector_path.png"):
    KM_PER_DEG_LAT = 111
    lat = wind_data["lat"].iloc[0]
    lon = wind_data["lon"].iloc[0]

    positions = [(lat, lon)]

    for _, row in wind_data.iterrows():
        speed_kmph = row["wind_speed_mps"] * 3.6
        angle_rad = math.radians(row["wind_direction_deg"])

        delta_lat = (speed_kmph * math.cos(angle_rad)) / KM_PER_DEG_LAT
        delta_lon = (speed_kmph * math.sin(angle_rad)) / (KM_PER_DEG_LAT * math.cos(math.radians(lat)))

        lat += delta_lat
        lon += delta_lon
        positions.append((lat, lon))

    lats, lons = zip(*positions)

    plt.figure(figsize=(8, 6))
    plt.plot(lons, lats, marker='o', linestyle='-', color='green')
    plt.title("Raw Wind Vector Path (24-Hour)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
