from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from wind_fetcher import fetch_wind_data
from simulator import simulate_dispersion
from visualizer import plot_dispersion, plot_wind_pattern, plot_wind_vectors
import os

app = Flask(__name__)
CORS(app)

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

        # Simulate particle spread (now returns total_hours as 4th value)
        path, total_distance, max_wind, total_hours = simulate_dispersion(wind_data, material_type=material)

        # Generate plots
        plot_dispersion(path, output_path=os.path.join(OUTPUT_DIR, "spread_plot.png"))
        plot_wind_pattern(wind_data, output_path=os.path.join(OUTPUT_DIR, "wind_pattern.png"))
        plot_wind_vectors(wind_data, output_path=os.path.join(OUTPUT_DIR, "wind_vector.png"))

        return jsonify({
            "spread_plot": "/outputs/spread_plot.png",
            "wind_pattern": "/outputs/wind_pattern.png",
            "wind_vector_path": "/outputs/wind_vector.png",
            "stats": {
                "distance_km": total_distance,
                "max_wind_speed": max_wind,
                "total_hours": total_hours
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
    port = int(os.environ.get("PORT", 5000))  # ✅ important for Render/Railway deployment
    app.run(host="0.0.0.0", port=port)