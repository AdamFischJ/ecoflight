async function runSimulation() {
  const lat = document.getElementById("lat").value;
  const lon = document.getElementById("lon").value;
  const material = document.getElementById("material").value;

  if (!lat || !lon) {
    alert("Please enter valid coordinates.");
    return;
  }

  document.getElementById("loading").style.display = "block";
  document.getElementById("stats").style.display = "none";

  try {
    const res = await fetch("http://127.0.0.1:5000/simulate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lat, lon, material })
    });

    const data = await res.json();

    if (data.error) {
      alert("Error: " + data.error);
      return;
    }

    const t = `?t=${Date.now()}`;
    document.getElementById("spreadImg").src = "http://127.0.0.1:5000" + data.spread_plot + t;
    document.getElementById("windPatternImg").src = "http://127.0.0.1:5000" + data.wind_pattern + t;
    document.getElementById("windVectorImg").src = "http://127.0.0.1:5000" + data.wind_vector_path + t;

    document.getElementById("stats").innerHTML = `
      <strong>Material:</strong> ${material}<br>
      <strong>Distance Traveled:</strong> ${data.stats.distance_km.toFixed(2)} km<br>
      <strong>Max Wind Speed:</strong> ${data.stats.max_wind_speed.toFixed(2)} m/s<br>
      <strong>Total Simulation Time:</strong> ${data.stats.hours} hours
    `;
    document.getElementById("stats").style.display = "block";

  } catch (err) {
    alert("Simulation failed.");
    console.error(err);
  } finally {
    document.getElementById("loading").style.display = "none";
  }
}
