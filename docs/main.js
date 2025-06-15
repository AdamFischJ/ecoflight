const API_BASE_URL = "https://web-production-2a99a.up.railway.app";

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
    const res = await fetch(`${API_BASE_URL}/simulate`, {
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
    document.getElementById("spreadImg").src = `${API_BASE_URL}${data.spread_plot.png}${t}`;
    document.getElementById("windPatternImg").src = `${API_BASE_URL}${data.wind_pattern.png}${t}`;
    document.getElementById("windVectorImg").src = `${API_BASE_URL}${data.wind_vector.png}${t}`;

    document.getElementById("stats").innerHTML = `
      <strong>Material:</strong> ${material}<br>
      <strong>Distance Traveled:</strong> ${data.stats.distance_km.toFixed(2)} km<br>
      <strong>Max Wind Speed:</strong> ${data.stats.max_wind_speed.toFixed(2)} m/s<br>
      <strong>Total Simulation Time:</strong> ${data.stats.total_hours} hours
    `;
    document.getElementById("stats").style.display = "block";

  } catch (err) {
    alert("Simulation failed.");
    console.error(err);
  } finally {
    document.getElementById("loading").style.display = "none";
  }
}