import pandas as pd
import random
from datetime import datetime, timedelta

def generate_mock_wind_data(lat, lon, hours=24):
    from datetime import datetime, timedelta, UTC
    base_time = datetime.now(UTC)
    data = []

    for i in range(hours):
        timestamp = base_time + timedelta(hours=i)
        wind_speed = round(random.uniform(1.0, 10.0), 2)
        wind_dir = round(random.uniform(0, 360), 1)
        data.append({
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'lat': lat,
            'lon': lon,
            'wind_speed_mps': wind_speed,
            'wind_direction_deg': wind_dir,
        })

    df = pd.DataFrame(data)
    df.to_csv('data/mock_wind_data.csv', index=False)
    return df