import matplotlib.pyplot as plt
import pandas as pd
import math
import os

def plot_dispersion(path, output_path="outputs/spread_plot.png"):
    lats, lons = zip(*path)
    plt.figure(figsize=(8, 6))
    plt.plot(lons, lats, marker='o', linestyle='-', color='blue')
    plt.scatter(lons[0], lats[0], color='green', label='Start')
    plt.scatter(lons[-1], lats[-1], color='red', label='End')
    plt.title("Simulated Particle Dispersion Path")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()

def plot_wind_pattern(df, output_path="outputs/wind_pattern.png"):
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.set_title("Wind Direction and Speed (Past 24 Hours)")
    ax1.plot(df["time"], df["wind_direction_deg"], 'bo-', label='Direction (°)')
    ax1.set_xlabel("Time (UTC)")
    ax1.set_ylabel("Wind Direction (°)", color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.tick_params(axis='x', rotation=90)

    ax2 = ax1.twinx()
    ax2.plot(df["time"], df["wind_speed_mps"], 'r--', label='Speed (m/s)')
    ax2.set_ylabel("Wind Speed (m/s)", color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    fig.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_wind_vectors(df, output_path="outputs/wind_vector_path.png"):
    KM_PER_DEG = 111
    start_lat = df["lat"].iloc[0]
    start_lon = df["lon"].iloc[0]
    lat = start_lat
    lon = start_lon
    points = [(lat, lon)]

    for _, row in df.iterrows():
        speed = row["wind_speed_mps"] * 3.6  # m/s to km/h
        direction = math.radians(row["wind_direction_deg"])
        delta_lat = (speed * math.cos(direction)) / KM_PER_DEG
        delta_lon = (speed * math.sin(direction)) / (KM_PER_DEG * math.cos(math.radians(lat)))
        lat += delta_lat
        lon += delta_lon
        points.append((lat, lon))

    lats, lons = zip(*points)
    plt.figure(figsize=(8, 6))
    plt.plot(lons, lats, marker='o', linestyle='-', color='green')
    plt.title("Raw Wind Vector Path (24-Hour)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
