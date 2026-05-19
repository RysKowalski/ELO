const API_BASE = "";

async function loadPlayers() {
  const response = await fetch(
    `${API_BASE}/api/get_players`
  );

  const data = await response.json();

  const playersList = document.getElementById(
    "playersList"
  );

  playersList.innerHTML = "";

  for (const [name, info] of Object.entries(data)) {
    const item = document.createElement("li");

    item.textContent =
      `${name} | ` +
      `ELO: ${info.elo} | ` +
      `Games: ${info.total_games} | ` +
      `Wins: ${info.wins} | ` +
      `Losses: ${info.loses}`;

    playersList.appendChild(item);
  }
}

async function submitGame(
  event
) {
  event.preventDefault();

  const player1 = document.getElementById(
    "player1"
  ).value;

  const player2 = document.getElementById(
    "player2"
  ).value;

  const result = document.getElementById(
    "result"
  ).value;

  const params = new URLSearchParams({
    player1,
    player2,
    result
  });

  const response = await fetch(
    `${API_BASE}/api/game?${params.toString()}`,
    {
      method: "POST"
    }
  );

  const data = await response.json();

  document.getElementById(
    "responseOutput"
  ).textContent = JSON.stringify(
    data,
    null,
    2
  );

  await loadPlayers();
}

document
  .getElementById("gameForm")
  .addEventListener(
    "submit",
    submitGame
  );

loadPlayers();
