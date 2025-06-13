from wind_fetcher import generate_mock_wind_data

def main():
    # Coordinates for Wilmington, NC
    lat = 34.2257
    lon = -77.9447

    print("Fetching simulated wind data for the last 24 hours...")
    wind_data = generate_mock_wind_data(lat, lon)

    print("\nFirst 5 rows of wind data:")
    print(wind_data.head())

if __name__ == "__main__":
    main()