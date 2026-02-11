let selectedFleetId = null;
let dynastyId = localStorage.getItem("selectedDynastyId");

async function loadFleetList() {
    const dynasties = await apiGet("/dynasties/");
  const list = document.getElementById("dynastyList");
  list.innerHTML = "";

  dynasties.forEach(name => {
    const li = document.createElement("li");
    li.textContent = name;
    li.classList.add("dynasty-item");

    li.onclick = () => {
      // Remove highlight from all
      document.querySelectorAll(".dynasty-item").forEach(el => el.classList.remove("selected"));

      // Highlight this one
      li.classList.add("selected");

      // Store selected
      selectedDynasty = name;
    };

    list.appendChild(li);
  });
}

function selectFleet(id, el) {
    document.querySelectorAll(".fleet").forEach(s => s.classList.remove("selected"));
    el.classList.add("selected");
    selectedFleetId = id;
}

function createFleet() {
    const name = prompt("Enter fleet name:");
    if (!name) return;

    fetch(`${API}/ships/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            dynasty_id: dynastyId,
            name: name
        })
    }).then(loadFleets);
}

function loadFleet() {
    if (!selectedFleetId) return alert("Select a fleet first.");
    window.location.href = `ship_detail.html?ship_id=${selectedFleetId}`;
}

function copyFleet() {
    if (!selectedFleetId) return alert("Select a fleet first.");
    fetch(`${API}/ships/copy/${selectedFleetId}`, { method: "POST" })
        .then(loadFleets);
}

function deleteFleet() {
    if (!selectedFleetId) return alert("Select a fleet first.");
    fetch(`${API}/ships/${selectedFleetId}`, { method: "DELETE" })
        .then(() => {
            selectedFleetId = null;
            loadFleets();
        });
}

loadFleets();