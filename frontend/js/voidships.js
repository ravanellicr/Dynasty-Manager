let selectedShipId = null;
let selectedFleetId = null;


/* ===============================
   GET URL PARAMETERS
================================= */
function getParams() {
    return new URLSearchParams(window.location.search);
}


/* ===============================
   LOAD SHIP LIST (BY FLEET)
================================= */
async function loadShipList() {

    const params = getParams();
    selectedFleetId = params.get("fleet_id");

    if (!selectedFleetId) {
        alert("No fleet selected.");
        return;
    }

    try {
        const ships = await apiGet(`/ships/fleet/${selectedFleetId}`);
        const list = document.getElementById("shipList");
        list.innerHTML = "";

        ships.forEach(ship => {
            const li = document.createElement("li");
            li.textContent = ship.name;
            li.classList.add("ship-item");
            li.dataset.shipId = ship.id;  // Store ship ID in data attribute

            li.onclick = () => selectShip(li, ship.id);

            list.appendChild(li);
        });

        // Restore selection from localStorage if exists
        //restoreSelection();

    } catch (error) {
        console.error("Error loading ships:", error);
        alert("Error loading ship list.");
    }
}


/* ===============================
   SELECT SHIP
================================= */
function selectShip(element, shipId) {

    // Remove selection from all items
    document.querySelectorAll(".ship-item")
        .forEach(el => el.classList.remove("selected"));

    // Add selection to clicked item
    element.classList.add("selected");

    // Update selected ship ID
    selectedShipId = shipId;
    localStorage.setItem("selectedShipId", shipId);
}


/* ===============================
   RESTORE SELECTION FROM LOCALSTORAGE
================================= */
function restoreSelection() {
    const savedShipId = localStorage.getItem("selectedShipId");
    
    if (savedShipId) {
        selectedShipId = parseInt(savedShipId);
        
        // Find and select the ship item
        const shipItems = document.querySelectorAll(".ship-item");
        shipItems.forEach(item => {
            if (parseInt(item.dataset.shipId) === selectedShipId) {
                item.classList.add("selected");
            }
        });
    }
}


/* ===============================
   CREATE SHIP (CREATE DB ENTRY THEN OPEN EDITOR)
================================= */
async function createShip() {

    if (!selectedFleetId) {
        alert("No fleet selected.");
        return;
    }

    try {
        // Create the ship in database first
        const newShip = await apiPost(`/ships`, { 
            fleet_id: selectedFleetId
        });

        // Redirect to editor with the new ship's ID
        window.location.href = `/voidship_details?ship_id=${newShip.id}`;

    } catch (error) {
        alert("Error creating ship.");
        console.error(error);
    }
}


/* ===============================
   LOAD SHIP (OPEN EDITOR WITH DATA)
================================= */
async function loadShip() {

    if (!selectedShipId) {
        return alert("Select a ship first.");
    }

    try {
        // Verify ship exists before redirecting
        await apiGet(`/ships/${selectedShipId}`);
        
        // Redirect to editor
        window.location.href = `/voidship_details?ship_id=${selectedShipId}`;
        
    } catch (error) {
        alert("Ship not found or error loading.");
        console.error(error);
        
        // Clear invalid selection
        selectedShipId = null;
        localStorage.removeItem("selectedShipId");
        await loadShipList();
    }
}


/* ===============================
   COPY SHIP
================================= */
async function copyShip() {

    if (!selectedShipId) {
        return alert("Select a ship first.");
    }

    try {
        // Copy the ship on backend
        const copiedShip = await apiPost(`/ships/${selectedShipId}/copy`, {});
        
        // Reload the ship list
        await loadShipList();
        
        // Select the newly copied ship
        selectedShipId = copiedShip.id;
        localStorage.setItem("selectedShipId", copiedShip.id);
        
        // Highlight the copied ship in the list
        const shipItems = document.querySelectorAll(".ship-item");
        shipItems.forEach(item => {
            if (parseInt(item.dataset.shipId) === copiedShip.id) {
                item.classList.add("selected");
            }
        });
        
        alert(`Ship copied successfully: ${copiedShip.name}`);

    } catch (error) {
        alert("Error copying ship.");
        console.error(error);
    }
}


/* ===============================
   DELETE SHIP
================================= */
async function deleteShip() {

    if (!selectedShipId) {
        return alert("Select a ship first.");
    }

    if (!confirm("Are you sure you want to delete this ship?")) {
        return;
    }

    try {
        await apiDelete(`/ships/${selectedShipId}`);

        // Clear selection
        selectedShipId = null;
        localStorage.removeItem("selectedShipId");

        // Reload the list
        await loadShipList();
        
        alert("Ship deleted successfully.");

    } catch (error) {
        alert("Error deleting ship.");
        console.error(error);
    }
}


/* ===============================
   AUTO LOAD ON PAGE OPEN
================================= */
document.addEventListener("DOMContentLoaded", loadShipList);