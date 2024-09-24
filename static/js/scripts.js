document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('input[name="inputType"]').forEach((elem) => {
        elem.addEventListener("change", function(event) {
            if (event.target.value === "manual") {
                document.getElementById("manualInput").style.display = "block";
                document.getElementById("csvInput").style.display = "none";
            } else {
                document.getElementById("manualInput").style.display = "none";
                document.getElementById("csvInput").style.display = "block";
            }
        });
    });
});

const formHandlers = {
    manual: handleManualInput,
    csv: handleCsvInput
};

function fetchWithTimeout(url, options, timeout = 5000) {
    return Promise.race([
        fetch(url, options),
        new Promise((_, reject) =>
            setTimeout(() => reject(new Error('Timeout after ' + timeout + 'ms')), timeout)
        )
    ]);
}

function submitForm() {
    const form = document.getElementById("teamForm");
    const formData = new FormData(form);
    const inputType = formData.get("inputType");

    const handler = formHandlers[inputType];
    if (handler) {
        handler(formData);
    }
}

function handleManualInput(formData) {
    const players = [];
    for (let i = 0; i < formData.getAll("player_name").length; i++) {
        players.push({
            name: formData.getAll("player_name")[i],
            rating: parseFloat(formData.getAll("player_rating")[i]),
            is_going: formData.getAll("is_going")[i] === "on" ? 1 : 0
        });
    }
    const teamCount = formData.get("teamCount");

    fetchWithTimeout("/generate_teams", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ players, teamCount }),
    },10000)
    .then(response => response.json())
    .then(data => {
        displayTeams(data);
    })
    .catch(error => console.error("Error:", error));
}

function handleCsvInput(formData) {
    const csvFile = formData.get("csvFile");
    const teamCount = formData.get("teamCount");

    const fileData = new FormData();
    fileData.append("csvFile", csvFile);
    fileData.append("teamCount", teamCount);

    fetchWithTimeout("/upload_csv", {
        method: "POST",
        body: fileData,
    }, 10000)
    .then(response => response.json())
    .then(data => {
        displayTeams(data);
    })
    .catch(error => console.error("Error:", error));
}

function displayTeams(data) {
    const teamsDiv = document.getElementById("teams");
    const teamsSection = document.getElementById("teams-section");
    teamsDiv.innerHTML = "";
    const teamsContainer = document.createElement("div");
    teamsContainer.className = "teams-container";
    data.forEach((team, index) => {
        const teamDiv = document.createElement("div");
        teamDiv.className = "team";
        teamDiv.innerHTML = `<h3>Team ${index + 1}</h3><ul>${team.map(member =>
            `<li>${member.player} (${member.rating})</li>`
        ).join('')}</ul>`;
        teamsContainer.appendChild(teamDiv);
    });
    teamsDiv.appendChild(teamsContainer);
    teamsSection.style.display = "block";
}

function addRow() {
    const playersDiv = document.getElementById("players");
    const playerRow = document.createElement("div");
    playerRow.className = "row";
    playerRow.innerHTML = `
        <div class="input-field col s3">
            <input type="text" name="player_name" placeholder="Player Name" required>
        </div>
        <div class="input-field col s3">
            <input type="number" name="player_rating" placeholder="Rating" step="0.1" min="0" max="5" required>
        </div>
        <div class="input-field col s2">
            <label>
                <input type="checkbox" name="is_going">
                <span>Is Going</span>
            </label>
        </div>
    `;
    playersDiv.appendChild(playerRow);
}