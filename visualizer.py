import matplotlib.pyplot as plt

def plot_path(path_coords, output_path="outputs/spread_plot.png"):
    """
    Plots the simulated path of material spread using matplotlib.

    Args:
        path_coords (list): List of (lat, lon) tuples
        output_path (str): Path to save the output image
    """
    if not path_coords or len(path_coords) < 2:
        print("Not enough points to plot.")
        return

    lats = [coord[0] for coord in path_coords]
    lons = [coord[1] for coord in path_coords]

    plt.figure(figsize=(10, 6))
    plt.plot(lons, lats, marker='o', linestyle='-', color='blue', linewidth=2, markersize=4)
    plt.scatter(lons[0], lats[0], color='green', label='Start', s=100, zorder=5)
    plt.scatter(lons[-1], lats[-1], color='red', label='End', s=100, zorder=5)

    plt.title("Simulated Wind-Carried Spread Path")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.grid(True)

    plt.savefig(output_path)
    plt.close()
    print(f"Plot saved to {output_path}")
