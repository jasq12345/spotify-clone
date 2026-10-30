const API = "http://127.0.0.1:8000";

const DEMO_SONGS = {
  songsCount: 4,
  songs: {
    1: { title: "I Was Made For Lovin' You", artist: "KISS", duration: 271, album: "Dynasty" },
    2: { title: "To Brazil!", artist: "Vengaboys", duration: 187, album: "The Platinum Album" },
    3: { title: "Touch Me", artist: "Günther", duration: 219, album: "Pleasureman" },
    4: { title: "Boys (Summertime Love)", artist: "Sabrina", duration: 234, album: "Sabrina" },
  },
};

const state = {
  queue: [],
  current: null,
  filter: "",
};

const el = {
  tracksBody: document.querySelector("#tracks-body"),
  search: document.querySelector("#search-input"),
  libraryCount: document.querySelector("#queue-music-count"),
  heroCount: document.querySelector("#hero-count"),
  playerTitle: document.querySelector("#title-music"),
  playerArtist: document.querySelector("#author-music"),
  npTitleTop: document.querySelector("#np-title-top"),
  npTitle: document.querySelector("#np-title"),
  npArtist: document.querySelector("#np-artist"),
  queueTitle: document.querySelector("#queue-title"),
  queueArtist: document.querySelector("#queue-artist"),
  duration: document.querySelector("#duration-music"),
  toast: document.querySelector("#toast"),
  addDialog: document.querySelector("#add-dialog"),
  addForm: document.querySelector("#add-form"),
};

let toastTimer;

function showToast(message, isError = false) {
  el.toast.textContent = message;
  el.toast.classList.toggle("error", isError);
  el.toast.hidden = false;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => {
    el.toast.hidden = true;
  }, 3000);
}

async function api(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API}${path}`, options);
  } catch {
    throw new Error("Backend unreachable or request failed");
  }
  if (!response.ok) {
    let message = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      if (typeof body.detail === "string") {
        message = body.detail;
      }
    } catch {
      message = `Request failed (${response.status})`;
    }
    throw new Error(message);
  }
  return response.json();
}

function sendJson(path, method, body) {
  return api(path, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

function formatTime(seconds) {
  const total = Math.max(0, Math.floor(Number(seconds) || 0));
  const min = Math.floor(total / 60);
  const sec = String(total % 60).padStart(2, "0");
  return `${min}:${sec}`;
}

function parseDuration(text) {
  const value = text.trim();
  if (!value) {
    return 0;
  }
  if (value.includes(":")) {
    const [min, sec] = value.split(":").map(Number);
    return (min || 0) * 60 + (sec || 0);
  }
  return Math.floor(Number(value)) || 0;
}

function make(tag, className, text) {
  const node = document.createElement(tag);
  if (className) {
    node.className = className;
  }
  if (text !== undefined) {
    node.textContent = text;
  }
  return node;
}

function visibleRows() {
  const rows = state.current ? [{ song: state.current, playing: true }] : [];
  state.queue.forEach((song) => rows.push({ song, playing: false }));
  const query = state.filter.trim().toLowerCase();
  if (!query) {
    return rows;
  }
  return rows.filter(({ song }) => `${song.title} ${song.artist}`.toLowerCase().includes(query));
}

function buildRow(song, playing, number) {
  const row = make("tr", playing ? "playing" : "");
  row.dataset.id = song.id;

  const info = make("div");
  info.append(make("p", "title", song.title), make("p", "subtitle", song.artist));
  const songBox = make("div", "song");
  songBox.append(make("div", "no-cover"), info);
  const songCell = make("td");
  songCell.append(songBox);

  const remove = make("button", "row-delete", "✕");
  remove.title = "Remove song";
  remove.setAttribute("aria-label", `Remove ${song.title}`);
  remove.dataset.id = song.id;
  const timeBox = make("div", "time-cell");
  timeBox.append(make("span", "", formatTime(song.duration)), remove);
  const timeCell = make("td");
  timeCell.append(timeBox);

  row.append(
    make("td", "", String(number)),
    songCell,
    make("td", "hide-mobile", song.album || "—"),
    make("td", "hide-mobile", "—"),
    timeCell
  );
  return row;
}

function renderTable() {
  const rows = visibleRows();
  el.tracksBody.replaceChildren();
  if (rows.length === 0) {
    const row = make("tr");
    const cell = make("td", "empty", state.filter ? "No songs match your search" : "Queue is empty");
    cell.colSpan = 5;
    row.append(cell);
    el.tracksBody.append(row);
    return;
  }
  rows.forEach(({ song, playing }, index) => {
    el.tracksBody.append(buildRow(song, playing, index + 1));
  });
}

function renderPlayer() {
  const song = state.current;
  const title = song ? song.title : "Nothing playing";
  const artist = song ? song.artist : "—";
  el.playerTitle.textContent = title;
  el.playerArtist.textContent = artist;
  el.npTitleTop.textContent = title;
  el.npTitle.textContent = title;
  el.npArtist.textContent = artist;
  el.duration.textContent = formatTime(song ? song.duration : 0);

  const next = state.queue[0];
  el.queueTitle.textContent = next ? next.title : "Nothing queued";
  el.queueArtist.textContent = next ? next.artist : "—";
}

function renderCounts() {
  const total = state.queue.length + (state.current ? 1 : 0);
  const label = `${total} ${total === 1 ? "song" : "songs"}`;
  el.libraryCount.textContent = label;
  el.heroCount.textContent = label;
}

function render() {
  renderTable();
  renderPlayer();
  renderCounts();
}

async function refresh() {
  const [list, current] = await Promise.all([api("/queue"), api("/navigation/current")]);
  state.queue = list.songs;
  state.current = current.song;
  render();
}

async function init() {
  try {
    await refresh();
    if (state.queue.length === 0 && !state.current) {
      await sendJson("/queue/setup", "POST", DEMO_SONGS);
      await refresh();
    }
  } catch (error) {
    render();
    showToast(error.message, true);
  }
}

async function goNext() {
  const data = await api("/navigation/next", { method: "POST" });
  if (data.message) {
    showToast(data.message);
  }
  await refresh();
}

async function goPrev() {
  const data = await api("/navigation/prev", { method: "POST" });
  if (data.message) {
    showToast(data.message);
  }
  await refresh();
}

async function shuffle() {
  await api("/navigation/shuffle", { method: "POST" });
  await refresh();
  showToast("Queue shuffled");
}

async function play() {
  if (!state.current) {
    await goNext();
  }
}

async function removeSong(id) {
  if (state.current && state.current.id === id) {
    await api("/navigation/current", { method: "DELETE" });
  } else {
    await api(`/editing/remove/${encodeURIComponent(id)}`, { method: "DELETE" });
  }
  await refresh();
  showToast("Song removed");
}

async function addSong() {
  const form = new FormData(el.addForm);
  const title = String(form.get("title")).trim();
  const artist = String(form.get("artist")).trim();
  if (!title || !artist) {
    showToast("Title and artist are required", true);
    return;
  }
  const song = {
    title,
    artist,
    album: String(form.get("album")).trim(),
    duration: parseDuration(String(form.get("duration"))),
  };
  const last = state.queue[state.queue.length - 1];
  if (last) {
    await sendJson("/editing/insert-after", "POST", { new_song: song, selected_song_id: last.id });
  } else {
    await sendJson("/editing/append", "POST", song);
  }
  el.addForm.reset();
  el.addDialog.close();
  await refresh();
  showToast("Song added");
}

let busy = false;

async function safely(task) {
  if (busy) {
    return;
  }
  busy = true;
  try {
    await task();
  } catch (error) {
    showToast(error.message, true);
  } finally {
    busy = false;
  }
}

document.querySelector("#btn-next").addEventListener("click", () => safely(goNext));
document.querySelector("#btn-prev").addEventListener("click", () => safely(goPrev));
document.querySelector("#btn-play").addEventListener("click", () => safely(play));
document.querySelector("#btn-play-big").addEventListener("click", () => safely(play));
document.querySelector("#btn-shuffle").addEventListener("click", () => safely(shuffle));
document.querySelector("#btn-shuffle-big").addEventListener("click", () => safely(shuffle));
document.querySelector("#btn-add").addEventListener("click", () => el.addDialog.showModal());
document.querySelector("#add-cancel").addEventListener("click", () => el.addDialog.close());
el.addForm.addEventListener("submit", (event) => {
  event.preventDefault();
  safely(addSong);
});

el.search.addEventListener("input", (event) => {
  state.filter = event.target.value;
  renderTable();
});

el.tracksBody.addEventListener("click", (event) => {
  const button = event.target.closest(".row-delete");
  if (button) {
    safely(() => removeSong(button.dataset.id));
  }
});

init();
