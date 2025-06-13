from wind_fetcher import fetch_wind_data
from simulator import simulate_dispersion
from visualizer import plot_dispersion

def main():
    # Coordinates for Wilmington, NC
    lat = 34.2257
    lon = -77.9447

    print("Fetching real wind data for the past 24 hours...")
    wind_data = fetch_wind_data(lat, lon)

    print("\nFirst 5 rows of wind data:")
    print(wind_data.head())

    print("\nRunning simulation...")
    particle_positions = simulate_dispersion(wind_data)

    print("Creating plot...")
    plot_dispersion(particle_positions)

    print("\n✅ Simulation complete. Plot saved to outputs/spread_plot.png")

if __name__ == "__main__":
    main()