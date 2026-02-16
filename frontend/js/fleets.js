let selectedFleetId = null;

/* ===============================
   LOAD FLEET LIST
================================= */
async function loadFleetList() {

    try {
        const fleets = await apiGet("/fleets/");
        const list = document.getElementById("fleetList");
        list.innerHTML = "";

        fleets.forEach(fleet => {
            const li = document.createElement("li");
            li.textContent = `${fleet.name} (${fleet.ship_count} ships)`;
            li.classList.add("fleet-item");

            li.onclick = () => selectFleet(li, fleet.id);

            list.appendChild(li);
        });

    } catch (error) {
        console.error("Error loading fleets:", error);
    }
}


/* ===============================
   SELECT FLEET
================================= */
function selectFleet(element, fleetId) {

    document.querySelectorAll(".fleet-item")
        .forEach(el => el.classList.remove("selected"));

    element.classList.add("selected");

    selectedFleetId = fleetId;

    localStorage.setItem("selectedFleetId", fleetId);
}


/* ===============================
   CREATE FLEET
================================= */
async function createFleet() {

    const name = prompt("Enter Fleet Name:");
    if (!name) return;

    try {
        await apiPost("/fleets/", { name });

        selectedFleetId = null;
        await loadFleetList();

    } catch (error) {
        alert("Error creating fleet.");
        console.error(error);
    }
}


/* ===============================
   LOAD FLEET DETAIL
================================= */
function loadFleet() {

    if (!selectedFleetId)
        return alert("Select a fleet first.");

    window.location.href =
        `/voidships?fleet_id=${selectedFleetId}`;
}


/* ===============================
   COPY FLEET
================================= */
async function copyFleet() {

    if (!selectedFleetId)
        return alert("Select a fleet first.");

    try {
        await apiPost(`/fleets/${selectedFleetId}/copy`, {});
        selectedFleetId = null;
        await loadFleetList();

    } catch (error) {
        alert("Error copying fleet.");
        console.error(error);
    }
}


/* ===============================
   DELETE FLEET
================================= */
async function deleteFleet() {

    if (!selectedFleetId)
        return alert("Select a fleet first.");

    if (!confirm("Are you sure you want to delete this fleet?"))
        return;

    try {
        await apiDelete(`/fleets/${selectedFleetId}`);

        selectedFleetId = null;
        localStorage.removeItem("selectedFleetId");

        await loadFleetList();

    } catch (error) {
        alert("Error deleting fleet.");
        console.error(error);
    }
}


/* ===============================
   AUTO LOAD ON PAGE OPEN
================================= */
document.addEventListener("DOMContentLoaded", loadFleetList);
