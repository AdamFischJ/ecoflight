from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from wind_fetcher import fetch_wind_data
from simulator import simulate_dispersion
from visualizer import plot_dispersion, plot_wind_pattern, plot_wind_vectors
import os

app = Flask(__name__, static_folder="web", template_folder="web")
CORS(app)

OUTPUT_DIR = "outputs"

@app.route("/simulate", methods=["POST"])
def simulate():
    try:
        lat = float(request.json.get("lat"))
        lon = float(request.json.get("lon"))
        material = request.json.get("material", "smoke")
        print(f"Simulating: lat={lat}, lon={lon}, material={material}")

        wind_data = fetch_wind_data(lat, lon)
        path, total_distance, max_wind = simulate_dispersion(wind_data, material_type=material)

        plot_dispersion(path, os.path.join(OUTPUT_DIR, "spread_plot.png"))
        plot_wind_pattern(wind_data, os.path.join(OUTPUT_DIR, "wind_pattern.png"))
        plot_wind_vectors(wind_data, os.path.join(OUTPUT_DIR, "wind_vector_path.png"))

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
def get_outputs(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    # serve other static files
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)