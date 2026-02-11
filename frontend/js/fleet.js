let selectedShipId = null;
let dynastyId = localStorage.getItem("selectedDynastyId");

async function loadShips() {
    if (!dynastyId) {
        document.getElementById("fleetList").innerHTML = "No dynasty selected.";
        return;
    }

    const res = await fetch(`${API}/ships/dynasty/${dynastyId}`);
    const ships = await res.json();

    const grouped = {};

    ships.forEach(ship => {
        const type = ship.hull_type || "Unassigned";
        if (!grouped[type]) grouped[type] = [];
        grouped[type].push(ship);
    });

    let html = "";

    for (const type in grouped) {
        html += `<div class="ship-type"><h3>${type}</h3>`;
        grouped[type].forEach(ship => {
            html += `<div class="ship" onclick="selectShip(${ship.id}, this)">
                        ${ship.name}
                     </div>`;
        });
        html += `</div>`;
    }

    document.getElementById("fleetList").innerHTML = html || "No ships in this dynasty.";
}

function selectShip(id, el) {
    document.querySelectorAll(".ship").forEach(s => s.classList.remove("selected"));
    el.classList.add("selected");
    selectedShipId = id;
}

function createShip() {
    const name = prompt("Enter ship name:");
    if (!name) return;

    fetch(`${API}/ships/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            dynasty_id: dynastyId,
            name: name
        })
    }).then(loadShips);
}

function loadShip() {
    if (!selectedShipId) return alert("Select a ship first.");
    window.location.href = `ship_detail.html?ship_id=${selectedShipId}`;
}

function copyShip() {
    if (!selectedShipId) return alert("Select a ship first.");
    fetch(`${API}/ships/copy/${selectedShipId}`, { method: "POST" })
        .then(loadShips);
}

function deleteShip() {
    if (!selectedShipId) return alert("Select a ship first.");
    fetch(`${API}/ships/${selectedShipId}`, { method: "DELETE" })
        .then(() => {
            selectedShipId = null;
            loadShips();
        });
}

loadShips();