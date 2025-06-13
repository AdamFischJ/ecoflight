from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from wind_fetcher import fetch_wind_data
from simulator import simulate_dispersion
from visualizer import plot_dispersion, plot_wind_pattern, plot_wind_vector_path
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin access

OUTPUT_DIR = "outputs"

@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        lat = float(request.json.get("lat"))
        lon = float(request.json.get("lon"))
        material = request.json.get("material", "smoke")

        print(f"Simulating: lat={lat}, lon={lon}, material={material}")

        # Fetch wind data
        wind_data = fetch_wind_data(lat, lon)

        # Simulate dispersion based on material type
        path, total_distance, max_wind = simulate_dispersion(wind_data, material_type=material)

        # Generate plots
        plot_dispersion(path, output_path=os.path.join(OUTPUT_DIR, "spread_plot.png"))
        plot_wind_pattern(wind_data, output_path=os.path.join(OUTPUT_DIR, "wind_pattern.png"))
        plot_wind_vector_path(wind_data, output_path=os.path.join(OUTPUT_DIR, "wind_vector_path.png"))

        # Return results
        return jsonify({
            "spread_plot": "/outputs/spread_plot.png",
            "wind_pattern": "/outputs/wind_pattern.png",
            "wind_vector_path": "/outputs/wind_vector_path.png",
            "stats": {
                "distance_km": total_distance,
                "max_wind_speed": max_wind,
                "total_hours": len(wind_data)
            }
        })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

@app.route("/outputs/<filename>")
def get_output_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route("/", methods=["GET"])
def home():
    return "EcoFlight API is running."

if __name__ == "__main__":
    app.run(debug=True)