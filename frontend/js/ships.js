let selectedShipId = null;

async function createShip() {
    const ship = {
        name: document.getElementById("name").value,
        hull_type: document.getElementById("hull").value
    };

    await apiPost("/ships/", ship);
    loadShips();
}

async function loadShips() {
    const ships = await apiGet("/ships/");
    const list = document.getElementById("shipList");
    list.innerHTML = "";

    ships.forEach(s => {
        const li = document.createElement("li");
        li.innerHTML = `
            <strong>${s.name}</strong> — ${s.hull_type}
            <button onclick="event.stopPropagation(); copyShip(${s.id})">Copy</button>
            <button onclick="event.stopPropagation(); deleteShip(${s.id})">Delete</button>
        `;
        li.onclick = () => selectShip(s.id, s.name);
        list.appendChild(li);
    });
}

function selectShip(id, name) {
    selectedShipId = id;
    document.getElementById("componentSection").style.display = "block";
    document.getElementById("selectedShipName").innerText = "Components for " + name;
    loadComponents();
}

async function deleteShip(id) {
    await fetch(`http://127.0.0.1:8000/ships/${id}`, { method: "DELETE" });
    document.getElementById("componentSection").style.display = "none";
    loadShips();
}

async function copyShip(id) {
    await fetch(`http://127.0.0.1:8000/ships/copy/${id}`, { method: "POST" });
    loadShips();
}

async function addComponent() {
    const component = {
        ship_id: selectedShipId,
        name: document.getElementById("compName").value,
        type: document.getElementById("compType").value,
        power_usage: parseInt(document.getElementById("compPower").value)
    };

    await apiPost("/components/", component);
    loadComponents();
}

async function loadComponents() {
    const components = await apiGet(`/components/ship/${selectedShipId}`);
    const list = document.getElementById("componentList");
    list.innerHTML = "";

    components.forEach(c => {
        const li = document.createElement("li");
        li.textContent = `${c.name} (${c.type}) — Power: ${c.power_usage}`;
        list.appendChild(li);
    });
}

async function loadHulls() {
    const hulls = await api("/ships/hulls");
    const select = document.getElementById("hullSelect");
    select.innerHTML = "";

    hulls.forEach(hull => {
        const option = document.createElement("option");
        option.value = hull;
        option.textContent = hull;
        select.appendChild(option);
    });
}

loadHulls();
loadShips();