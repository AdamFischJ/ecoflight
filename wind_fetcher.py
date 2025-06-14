import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

def fetch_wind_data(lat, lon):
    """
    Fetches real hourly wind speed and direction data for the past 24 hours
    from the Open-Meteo API and returns it as a Pandas DataFrame.
    """
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=24)

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&hourly=wind_speed_10m,wind_direction_10m"
        f"&start={start_time.strftime('%Y-%m-%dT%H:00')}"
        f"&end={end_time.strftime('%Y-%m-%dT%H:00')}"
        f"&timezone=UTC"
    )

    print(f"Requesting wind data from Open-Meteo:\n{url}\n")
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code} {response.text}")

    data = response.json()

    # ✅ Confirm all fields exist
    if not all(k in data["hourly"] for k in ("time", "wind_speed_10m", "wind_direction_10m")):
        raise Exception("Missing one or more required keys in API response")

    df = pd.DataFrame({
        "time": pd.to_datetime(data["hourly"]["time"]),
        "wind_speed_mps": data["hourly"]["wind_speed_10m"],
        "wind_direction_deg": data["hourly"]["wind_direction_10m"],
    })

    df["lat"] = lat
    df["lon"] = lon

    return df