const API = "http://127.0.0.1:8000";

async function pobierzPlaylist() {
  const response = await fetch(`${API}/playlist`);
  const dane = await response.json();
  console.log(dane);
}

pobierzPlaylist();