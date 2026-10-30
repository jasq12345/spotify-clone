const API = "http://127.0.0.1:8000";

const DEMO_SONGS = {
  songs: {
    1: { title: "I Was Made For Lovin' You", artist: "KISS", duration: 271, album: "Dynasty" },
    2: { title: "To Brazil!", artist: "Vengaboys", duration: 187, album: "The Platinum Album" },
    3: { title: "Touch Me", artist: "Günther", duration: 219, album: "Pleasureman" },
    4: { title: "Boys (Summertime Love)", artist: "Sabrina", duration: 234, album: "Sabrina" },
  },
};

const DEMO_PLAYLISTS = [
  {
    name: "Polskie klasyki",
    songs: [
      { title: "Jolka, Jolka", artist: "Budka Suflera", duration: 318, album: "Za ostatni grosz" },
      { title: "Autobiografia", artist: "Perfect", duration: 287, album: "Unu" },
      { title: "Dziwny jest ten świat", artist: "Czesław Niemen", duration: 250 },
      { title: "Wehikuł czasu", artist: "Dżem", duration: 343 },
    ],
  },
  {
    name: "90s Eurodance",
    songs: [
      { title: "What Is Love", artist: "Haddaway", duration: 270 },
      { title: "Blue (Da Ba Dee)", artist: "Eiffel 65", duration: 283 },
      { title: "Rhythm Is a Dancer", artist: "Snap!", duration: 332 },
      { title: "Barbie Girl", artist: "Aqua", duration: 197 },
    ],
  },
  {
    name: "Rock Classics",
    songs: [
      { title: "Bohemian Rhapsody", artist: "Queen", duration: 354 },
      { title: "Hotel California", artist: "Eagles", duration: 391 },
      { title: "Stairway to Heaven", artist: "Led Zeppelin", duration: 482 },
      { title: "Smells Like Teen Spirit", artist: "Nirvana", duration: 301 },
    ],
  },
];

const SEEDED_KEY = "spotify-clone-demo-playlists";

const state = {
  view: "queue",
  history: [],
  current: null,
  queue: [],
  playlistsReady: true,
  playlists: [],
  playlistId: null,
  playlist: null,
  filter: "",
  playing: false,
  elapsed: 0,
  lastSongId: null,
  repeat: false,
  volume: 70,
  muted: false,
};

const el = {
  tracksBody: document.querySelector("#tracks-body"),
  search: document.querySelector("#search-input"),
  libQueue: document.querySelector("#lib-queue"),
  libQueueCount: document.querySelector("#lib-queue-count"),
  libPlaylists: document.querySelector("#lib-playlists"),
  libNote: document.querySelector("#lib-note"),
  newPlaylist: document.querySelector("#btn-new-playlist"),
  heroType: document.querySelector("#hero-type"),
  heroTitle: document.querySelector("#hero-title"),
  heroCount: document.querySelector("#hero-count"),
  clear: document.querySelector("#btn-clear"),
  rename: document.querySelector("#btn-rename"),
  deletePlaylist: document.querySelector("#btn-delete-playlist"),
  playerTitle: document.querySelector("#title-music"),
  playerArtist: document.querySelector("#author-music"),
  npTitleTop: document.querySelector("#np-title-top"),
  npTitle: document.querySelector("#np-title"),
  npArtist: document.querySelector("#np-artist"),
  queueTitle: document.querySelector("#queue-title"),
  queueArtist: document.querySelector("#queue-artist"),
  duration: document.querySelector("#duration-music"),
  time: document.querySelector("#time-music"),
  songBar: document.querySelector("#song-line"),
  songLine: document.querySelector("#song-line div"),
  volumeBar: document.querySelector("#volume-control"),
  volumeLine: document.querySelector("#volume-control div"),
  playIcon: document.querySelector("#btn-play img"),
  playBigIcon: document.querySelector("#btn-play-big img"),
  repeat: document.querySelector("#btn-repeat"),
  mute: document.querySelector("#btn-mute"),
  toast: document.querySelector("#toast"),
  songDialog: document.querySelector("#song-dialog"),
  songForm: document.querySelector("#song-form"),
  songDialogTitle: document.querySelector("#song-dialog-title"),
  songDialogSubmit: document.querySelector("#song-dialog-submit"),
  nameDialog: document.querySelector("#name-dialog"),
  nameForm: document.querySelector("#name-form"),
  nameDialogTitle: document.querySelector("#name-dialog-title"),
  pickDialog: document.querySelector("#pick-dialog"),
  pickSelect: document.querySelector("#pick-select"),
  confirmDialog: document.querySelector("#confirm-dialog"),
  confirmText: document.querySelector("#confirm-text"),
  confirmOk: document.querySelector("#confirm-ok"),
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

function errorMessage(body, status) {
  const detail = body && body.detail;
  if (typeof detail === "string") {
    return detail;
  }
  if (Array.isArray(detail) && detail.length > 0) {
    return detail.map((item) => item.msg).join(", ");
  }
  return `Request failed (${status})`;
}

async function api(path, options = {}) {
  let response;
  try {
    response = await fetch(`${API}${path}`, options);
  } catch {
    throw new Error("Backend unreachable or request failed");
  }
  let body = null;
  if (response.status !== 204) {
    try {
      body = await response.json();
    } catch {
      body = null;
    }
  }
  if (!response.ok) {
    const error = new Error(errorMessage(body, response.status));
    error.status = response.status;
    throw error;
  }
  return body ?? {};
}

async function onConflict(request, message) {
  try {
    return await request;
  } catch (error) {
    if (error.status === 409) {
      error.message = message;
    }
    throw error;
  }
}

function sendJson(path, method, body) {
  return api(path, {
    method,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
}

function post(path) {
  return api(path, { method: "POST" });
}

function remove(path) {
  return api(path, { method: "DELETE" });
}

function enc(value) {
  return encodeURIComponent(value);
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
    return null;
  }
  if (value.includes(":")) {
    const [min, sec] = value.split(":").map(Number);
    return Math.max(0, (min || 0) * 60 + (sec || 0));
  }
  return Math.max(0, Math.floor(Number(value)) || 0);
}

function pluralSongs(count) {
  return `${count} ${count === 1 ? "song" : "songs"}`;
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

function openDialog(dialog) {
  return new Promise((resolve) => {
    dialog.returnValue = "";
    dialog.addEventListener("close", () => resolve(dialog.returnValue === "ok"), { once: true });
    dialog.showModal();
  });
}

async function askConfirm(text, okLabel) {
  el.confirmText.textContent = text;
  el.confirmOk.textContent = okLabel;
  return openDialog(el.confirmDialog);
}

async function askName(title, value) {
  el.nameDialogTitle.textContent = title;
  el.nameForm.elements.name.value = value;
  if (!(await openDialog(el.nameDialog))) {
    return null;
  }
  return el.nameForm.elements.name.value.trim() || null;
}

async function askPlaylist() {
  const choices = state.playlists.filter((playlist) => playlist.id !== state.playlistId);
  if (choices.length === 0) {
    showToast(state.playlists.length ? "No other playlist to add to" : "Create a playlist first", true);
    return null;
  }
  el.pickSelect.replaceChildren(
    ...choices.map((playlist) => {
      const option = make("option", "", playlist.name);
      option.value = playlist.id;
      return option;
    })
  );
  if (!(await openDialog(el.pickDialog))) {
    return null;
  }
  return el.pickSelect.value;
}

async function askSong(title, submitLabel, song = null) {
  const fields = el.songForm.elements;
  el.songForm.reset();
  el.songDialogTitle.textContent = title;
  el.songDialogSubmit.textContent = submitLabel;
  el.songForm.querySelectorAll(".song-extra").forEach((input) => {
    input.hidden = song !== null;
  });
  if (song) {
    fields.title.value = song.title;
    fields.artist.value = song.artist;
  }
  if (!(await openDialog(el.songDialog))) {
    return null;
  }
  const result = {
    title: fields.title.value.trim(),
    artist: fields.artist.value.trim(),
  };
  if (!result.title || !result.artist) {
    showToast("Title and artist are required", true);
    return null;
  }
  const album = fields.album.value.trim();
  const duration = parseDuration(fields.duration.value);
  if (!song && album) {
    result.album = album;
  }
  if (!song && duration !== null) {
    result.duration = duration;
  }
  return result;
}

async function loadQueueSeparately() {
  const [queue, current, history] = await Promise.all([
    api("/queue"),
    api("/navigation/current"),
    api("/history").catch(() => ({ songs: [] })),
  ]);
  state.queue = queue.songs ?? [];
  state.current = current.song ?? null;
  state.history = (history.songs ?? []).slice().reverse();
}

async function loadQueue() {
  try {
    const data = await api("/queue/combined");
    state.history = data.history ?? [];
    state.current = data.current ?? null;
    state.queue = data.queue ?? [];
  } catch {
    await loadQueueSeparately();
  }
}

async function loadPlaylists() {
  try {
    const data = await api("/playlists");
    state.playlists = (data.playlists ?? []).slice().sort((a, b) => a.name.localeCompare(b.name));
    state.playlistsReady = true;
  } catch (error) {
    if (error.status === 404 || error.status === 405) {
      state.playlistsReady = false;
      state.playlists = [];
      return;
    }
    throw error;
  }
}

async function loadPlaylist() {
  if (state.view !== "playlist") {
    state.playlist = null;
    return;
  }
  try {
    state.playlist = await api(`/playlists/${enc(state.playlistId)}`);
  } catch (error) {
    if (error.status === 404) {
      state.view = "queue";
      state.playlistId = null;
      state.playlist = null;
      showToast("Playlist no longer exists", true);
      return;
    }
    throw error;
  }
}

async function refresh() {
  await Promise.all([loadQueue(), loadPlaylists(), loadPlaylist()]);
  render();
}

function queueRows() {
  const rows = state.history.map((song) => ({ song, kind: "history" }));
  if (state.current) {
    rows.push({ song: state.current, kind: "current" });
  }
  state.queue.forEach((song) => rows.push({ song, kind: "queue" }));
  return rows;
}

function playlistRows() {
  const songs = state.playlist ? state.playlist.songs ?? [] : [];
  return songs.map((song) => ({ song, kind: "playlist" }));
}

function visibleRows() {
  const rows = state.view === "playlist" ? playlistRows() : queueRows();
  const query = state.filter.trim().toLowerCase();
  if (!query) {
    return rows;
  }
  return rows.filter(({ song }) => `${song.title} ${song.artist}`.toLowerCase().includes(query));
}

function rowButton(action, symbol, label, song) {
  const button = make("button", "row-btn", symbol);
  button.dataset.action = action;
  button.dataset.id = song.id;
  button.title = label;
  button.setAttribute("aria-label", `${label}: ${song.title}`);
  return button;
}

function rowButtons(kind, song) {
  const buttons = [];
  if (kind === "history") {
    buttons.push(rowButton("replay", "↺", "Play next", song));
  }
  if (kind === "queue") {
    buttons.push(rowButton("edit", "✎", "Edit", song));
  }
  if (state.playlistsReady) {
    buttons.push(rowButton("add-to-playlist", "+", "Add to playlist", song));
  }
  if (kind === "current" || kind === "queue") {
    buttons.push(rowButton("remove", "✕", "Remove", song));
  }
  if (kind === "playlist") {
    buttons.push(rowButton("remove-from-playlist", "✕", "Remove from playlist", song));
  }
  return buttons;
}

function buildRow({ song, kind }, number) {
  const rowClass = kind === "current" ? "playing" : kind === "history" ? "played" : "";
  const row = make("tr", rowClass);
  row.dataset.id = song.id;

  const info = make("div");
  info.append(make("p", "title", song.title), make("p", "subtitle", song.artist));
  const songBox = make("div", "song");
  songBox.append(make("div", "no-cover"), info);
  const songCell = make("td");
  songCell.append(songBox);

  const actions = make("div", "row-actions");
  actions.append(...rowButtons(kind, song));
  const timeBox = make("div", "time-cell");
  timeBox.append(make("span", "", formatTime(song.duration)), actions);
  const timeCell = make("td");
  timeCell.append(timeBox);

  row.append(
    make("td", "", String(number)),
    songCell,
    make("td", "hide-mobile", song.album || "—"),
    make("td", "hide-mobile", song.added_at || "—"),
    timeCell
  );
  return row;
}

function emptyMessage() {
  if (state.filter.trim()) {
    return "No songs match your search";
  }
  return state.view === "playlist" ? "This playlist is empty" : "Queue is empty";
}

function renderTable() {
  const rows = visibleRows();
  el.tracksBody.replaceChildren();
  if (rows.length === 0) {
    const row = make("tr");
    const cell = make("td", "empty", emptyMessage());
    cell.colSpan = 5;
    row.append(cell);
    el.tracksBody.append(row);
    return;
  }
  rows.forEach((item, index) => {
    el.tracksBody.append(buildRow(item, index + 1));
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

  const songId = song ? song.id : null;
  if (songId !== state.lastSongId) {
    state.lastSongId = songId;
    state.elapsed = 0;
  }
  if (!song) {
    state.playing = false;
  }
  renderProgress();
  renderPlayButtons();
}

function songLength() {
  if (!state.current) {
    return 0;
  }
  return state.current.duration || 0;
}

function renderProgress() {
  const length = songLength();
  let percent = 0;
  if (length > 0) {
    percent = (state.elapsed / length) * 100;
  }
  el.time.textContent = formatTime(state.elapsed);
  el.songLine.style.width = percent + "%";
}

function renderPlayButtons() {
  let icon = "images/play.svg";
  if (state.playing) {
    icon = "images/pause.svg";
  }
  el.playIcon.src = icon;
  if (state.view === "playlist") {
    el.playBigIcon.src = "images/play.svg";
  } else {
    el.playBigIcon.src = icon;
  }
}

function renderVolume() {
  let width = state.volume;
  if (state.muted) {
    width = 0;
  }
  el.volumeLine.style.width = width + "%";
  el.mute.title = state.muted ? "Unmute" : "Mute";
}

function upcomingCount() {
  return state.queue.length + (state.current ? 1 : 0);
}

function renderHero() {
  const inPlaylist = state.view === "playlist" && state.playlist;
  el.heroType.textContent = inPlaylist ? "Playlist" : "Queue";
  el.heroTitle.textContent = inPlaylist ? state.playlist.name : "Queue";
  el.heroCount.textContent = pluralSongs(inPlaylist ? (state.playlist.songs ?? []).length : upcomingCount());
  el.clear.hidden = Boolean(inPlaylist);
  el.rename.hidden = !inPlaylist;
  el.deletePlaylist.hidden = !inPlaylist;
}

function buildPlaylistItem(playlist) {
  const active = state.view === "playlist" && state.playlistId === playlist.id;
  const item = make("button", active ? "playlist active" : "playlist");
  item.dataset.playlistId = playlist.id;
  const info = make("div");
  info.append(
    make("p", "title", playlist.name),
    make("p", "subtitle", `Playlist • ${pluralSongs(playlist.songsCount ?? 0)}`)
  );
  item.append(make("div", "no-cover"), info);
  return item;
}

function renderLibrary() {
  el.libQueue.classList.toggle("active", state.view === "queue");
  el.libQueueCount.textContent = pluralSongs(upcomingCount());
  el.libPlaylists.replaceChildren(...state.playlists.map(buildPlaylistItem));
  el.libNote.hidden = state.playlistsReady;
  el.newPlaylist.hidden = !state.playlistsReady;
}

function render() {
  renderTable();
  renderPlayer();
  renderHero();
  renderLibrary();
}

function wasSeeded() {
  try {
    return localStorage.getItem(SEEDED_KEY) === "yes";
  } catch {
    return false;
  }
}

function markSeeded() {
  try {
    localStorage.setItem(SEEDED_KEY, "yes");
  } catch {
    return;
  }
}

async function seedPlaylists() {
  for (const playlist of DEMO_PLAYLISTS) {
    const created = await sendJson("/playlists", "POST", { name: playlist.name });
    for (const song of playlist.songs) {
      await sendJson(`/playlists/${enc(created.id)}/songs`, "POST", song);
    }
  }
}

async function boot() {
  await refresh();
  let changed = false;
  if (state.playlistsReady && state.playlists.length === 0 && !wasSeeded()) {
    markSeeded();
    await seedPlaylists();
    changed = true;
  }
  if (!state.current && state.queue.length === 0 && state.history.length === 0) {
    await sendJson("/queue/setup", "POST", DEMO_SONGS);
    changed = true;
  }
  if (changed) {
    await refresh();
  }
}

async function goNext() {
  const data = await post("/navigation/next");
  if (data.message) {
    showToast(data.message);
  }
  await refresh();
}

async function goPrev() {
  if (state.elapsed > 3) {
    state.elapsed = 0;
    renderProgress();
    return;
  }
  const data = await post("/navigation/prev");
  if (data.message) {
    showToast(data.message);
  }
  await refresh();
}

async function shuffleQueue() {
  await post("/navigation/shuffle");
  await refresh();
  showToast("Queue shuffled");
}

async function playPlaylist(shuffled) {
  const name = state.playlist.name;
  if ((state.playlist.songs ?? []).length === 0) {
    showToast(`${name} is empty`, true);
    return;
  }
  await post(`/playlists/${enc(state.playlistId)}/play`);
  if (shuffled) {
    await post("/navigation/shuffle");
  }
  await post("/navigation/next");
  state.view = "queue";
  state.playlistId = null;
  state.playing = true;
  await refresh();
  showToast(`Playing ${name}`);
}

async function togglePlay() {
  if (state.current) {
    state.playing = !state.playing;
    renderPlayButtons();
    return;
  }
  await goNext();
  if (state.current) {
    state.playing = true;
    renderPlayButtons();
  }
}

async function playMain() {
  if (state.view === "playlist" && state.playlist) {
    await playPlaylist(false);
    return;
  }
  await togglePlay();
}

async function autoNext() {
  const oldId = state.current.id;
  await goNext();
  if (!state.current || state.current.id === oldId) {
    state.playing = false;
    renderPlayButtons();
  }
}

function tick() {
  if (!state.playing || !state.current) {
    return;
  }
  const length = songLength();
  state.elapsed = state.elapsed + 1;
  if (length > 0 && state.elapsed >= length) {
    if (state.repeat) {
      state.elapsed = 0;
    } else {
      state.elapsed = length;
      safely(autoNext);
    }
  }
  renderProgress();
}

function toggleRepeat() {
  state.repeat = !state.repeat;
  el.repeat.classList.toggle("on", state.repeat);
  showToast(state.repeat ? "Repeat on" : "Repeat off");
}

async function shuffleMain() {
  if (state.view === "playlist" && state.playlist) {
    await playPlaylist(true);
    return;
  }
  await shuffleQueue();
}

async function addSong() {
  const inPlaylist = state.view === "playlist" && state.playlist;
  const song = await askSong(inPlaylist ? `Add to ${state.playlist.name}` : "Add to queue", "Add");
  if (!song) {
    return;
  }
  if (inPlaylist) {
    await onConflict(
      sendJson(`/playlists/${enc(state.playlistId)}/songs`, "POST", song),
      "This song is already in the playlist"
    );
  } else {
    await sendJson("/editing/append", "POST", song);
  }
  await refresh();
  showToast("Song added");
}

async function editSong(songId) {
  const song = state.queue.find((item) => item.id === songId);
  if (!song) {
    return;
  }
  const changes = await askSong("Edit song", "Save", song);
  if (!changes) {
    return;
  }
  if (changes.title !== song.title) {
    await sendJson(`/editing/update-title/${enc(songId)}`, "PATCH", { new_title: changes.title });
  }
  if (changes.artist !== song.artist) {
    await sendJson(`/editing/update-artist/${enc(songId)}`, "PATCH", { new_artist: changes.artist });
  }
  await refresh();
  showToast("Song updated");
}

async function removeSong(songId) {
  if (state.current && state.current.id === songId) {
    await remove("/navigation/current");
  } else {
    await remove(`/editing/remove/${enc(songId)}`);
  }
  await refresh();
  showToast("Song removed");
}

async function replaySong(songId) {
  await post(`/history/${enc(songId)}/replay`);
  await refresh();
  showToast("Plays next");
}

async function addToPlaylist(songId) {
  const playlistId = await askPlaylist();
  if (!playlistId) {
    return;
  }
  const playlist = state.playlists.find((item) => item.id === playlistId);
  const name = playlist ? playlist.name : "the playlist";
  await onConflict(
    sendJson(`/playlists/${enc(playlistId)}/songs`, "POST", { song_id: songId }),
    `This song is already in ${name}`
  );
  await refresh();
  showToast(`Added to ${name}`);
}

async function removeFromPlaylist(songId) {
  await remove(`/playlists/${enc(state.playlistId)}/songs/${enc(songId)}`);
  await refresh();
  showToast("Removed from playlist");
}

async function clearQueue() {
  const ok = await askConfirm("This removes the queue, the history and the current song.", "Clear");
  if (!ok) {
    return;
  }
  await remove("/editing/remove-all");
  await refresh();
  showToast("Queue cleared");
}

function clearFilter() {
  state.filter = "";
  el.search.value = "";
}

async function openQueue() {
  clearFilter();
  state.view = "queue";
  state.playlistId = null;
  await refresh();
}

async function openPlaylist(playlistId) {
  clearFilter();
  state.view = "playlist";
  state.playlistId = playlistId;
  await refresh();
}

async function createPlaylist() {
  const name = await askName("New playlist", "");
  if (!name) {
    return;
  }
  const created = await onConflict(
    sendJson("/playlists", "POST", { name }),
    `A playlist named "${name}" already exists`
  );
  if (created.id) {
    await openPlaylist(created.id);
  } else {
    await refresh();
  }
  showToast(`Created ${name}`);
}

async function renamePlaylist() {
  const name = await askName("Rename playlist", state.playlist.name);
  if (!name || name === state.playlist.name) {
    return;
  }
  await onConflict(
    sendJson(`/playlists/${enc(state.playlistId)}`, "PATCH", { name }),
    `A playlist named "${name}" already exists`
  );
  await refresh();
  showToast("Playlist renamed");
}

async function deletePlaylist() {
  const ok = await askConfirm(`Delete "${state.playlist.name}"? The songs stay in other playlists.`, "Delete");
  if (!ok) {
    return;
  }
  await remove(`/playlists/${enc(state.playlistId)}`);
  state.view = "queue";
  state.playlistId = null;
  await refresh();
  showToast("Playlist deleted");
}

const rowActions = {
  replay: replaySong,
  edit: editSong,
  remove: removeSong,
  "add-to-playlist": addToPlaylist,
  "remove-from-playlist": removeFromPlaylist,
};

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
    if (error.status === 404 || error.status === 409) {
      await refresh().catch(() => render());
    }
  } finally {
    busy = false;
  }
}

function onClick(selector, task) {
  document.querySelector(selector).addEventListener("click", () => safely(task));
}

onClick("#btn-next", goNext);
onClick("#btn-prev", goPrev);
onClick("#btn-play", togglePlay);
onClick("#btn-play-big", playMain);
onClick("#btn-shuffle", shuffleQueue);
onClick("#btn-shuffle-big", shuffleMain);
onClick("#btn-add-song", addSong);
onClick("#btn-new-playlist", createPlaylist);
onClick("#btn-clear", clearQueue);
onClick("#btn-rename", renamePlaylist);
onClick("#btn-delete-playlist", deletePlaylist);
onClick("#btn-home", openQueue);
onClick("#lib-queue", openQueue);
onClick("#btn-open-queue", openQueue);

el.repeat.addEventListener("click", toggleRepeat);

el.mute.addEventListener("click", () => {
  state.muted = !state.muted;
  renderVolume();
});

el.volumeBar.addEventListener("click", (event) => {
  state.volume = Math.round((event.offsetX / el.volumeBar.offsetWidth) * 100);
  state.muted = false;
  renderVolume();
});

el.songBar.addEventListener("click", (event) => {
  const length = songLength();
  if (length === 0) {
    return;
  }
  state.elapsed = Math.floor((event.offsetX / el.songBar.offsetWidth) * length);
  renderProgress();
});

document.addEventListener("keydown", (event) => {
  if (event.code === "Space" && event.target === document.body) {
    event.preventDefault();
    safely(togglePlay);
  }
});

setInterval(tick, 1000);
renderVolume();

el.libPlaylists.addEventListener("click", (event) => {
  const item = event.target.closest("[data-playlist-id]");
  if (item) {
    safely(() => openPlaylist(item.dataset.playlistId));
  }
});

el.tracksBody.addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");
  if (button && rowActions[button.dataset.action]) {
    safely(() => rowActions[button.dataset.action](button.dataset.id));
  }
});

el.search.addEventListener("input", (event) => {
  state.filter = event.target.value;
  renderTable();
});

safely(async () => {
  try {
    await boot();
  } catch (error) {
    render();
    throw error;
  }
});