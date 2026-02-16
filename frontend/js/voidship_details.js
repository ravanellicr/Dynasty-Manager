/* ===============================
   GLOBAL STATE - TEMPORARY WORKING DATA
================================= */
let currentShipId = null;
let shipData = {
    // Essential Info
    ship_id: 0,
    fleet_id: 0, 

    // Basic Info
    name: "",
    hull_type: "",
    
    // Stats (working values that will be calculated)
    speed: 0,
    maneuver: 0,
    detection: 0,
    hull_integrity: 0,
    armor: 0,
    
    // Components
    essential_plasma_drive: "",
    essential_warp_drive: "",
    // ... etc
    
    // Calculated bonuses/modifiers
    speedBonus: 0,
    armorBonus: 0,
    // ... etc
};


/* ===============================
   GET URL PARAMETERS
================================= */
function getParams() {
    return new URLSearchParams(window.location.search);
}


/* ===============================
   LOAD SHIP DETAILS FROM DATABASE
================================= */
async function loadShipDetails() {
    const params = getParams();
    currentShipId = params.get("ship_id");

    if (!currentShipId) {
        alert("No ship ID provided.");
        window.location.href = "/voidships";
        return;
    }

    try {
        const ship = await apiGet(`/ships/${currentShipId}`);
        
        // Load data into temporary working object
        shipData.ship_id = ship.id ;
        shipData.fleet_id = ship.fleet_id ;

        shipData.name = ship.name || "";
        
        // ... load all other fields
        
        // Update UI with loaded data
        updateUI();

    } catch (error) {
        console.error("Error loading ship:", error);
        alert("Error loading ship details.");
    }
}


/* ===============================
   UPDATE UI FROM TEMPORARY DATA
================================= */
function updateUI() {
    // Update input fields
    document.getElementById("voidship_name").value = shipData.name;
    
    
    // ... update all other UI elements
}


/* ===============================
   UPDATE NAME IN TEMPORARY DATA
================================= */
function updateTempData() {
    const nameInput = document.getElementById("voidship_name");
    shipData.name = nameInput.value.trim();
    
    // Optional: Show unsaved changes indicator
    markAsUnsaved();
}


/* ===============================
   CALCULATE FINAL STATS
   (Call this whenever components change)
================================= */
function calculateStats() {
    // Example: Speed calculation
    // Base speed from hull + component bonuses
    shipData.speed = getBaseSpeed(shipData.hull_type) + shipData.speedBonus;
    
    // Armor calculation
    shipData.armor = getBaseArmor(shipData.hull_type) + shipData.armorBonus;
    
    // ... perform all mathematical operations here
    
    // Update the UI with new calculated values
    updateUI();
}


/* ===============================
   MARK AS UNSAVED (VISUAL FEEDBACK)
================================= */
function markAsUnsaved() {
    const saveButton = document.getElementById("saveButton");
    if (saveButton) {
        saveButton.classList.add("unsaved");
        saveButton.textContent = "Save Changes *";
    }
}

function markAsSaved() {
    const saveButton = document.getElementById("saveButton");
    if (saveButton) {
        saveButton.classList.remove("unsaved");
        saveButton.textContent = "Save Changes";
    }
}


/* ===============================
   SAVE ALL CHANGES TO DATABASE
================================= */
async function saveShip() {
    if (!currentShipId) {
        alert("No ship loaded.");
        return;
    }

    // Validate required fields
    if (!shipData.name.trim()) {
        alert("Ship name cannot be empty.");
        return;
    }

    try {
        // Send ONLY the final calculated values to backend
        const updatedShip = await apiPut(`/ships/${currentShipId}`, {
            name: shipData.name,
            
            // ... etc
        });

        alert("Ship saved successfully!");
        markAsSaved();

    } catch (error) {
        console.error("Error saving ship:", error);
        alert("Error saving ship: " + error.message);
    }
}


/* ===============================
   DISCARD CHANGES (RELOAD FROM DB)
================================= */
async function discardChanges() {
    if (confirm("Are you sure you want to discard all changes?")) {
        await loadShipDetails();
        markAsSaved();
    }
}


/* ===============================
   GO BACK WITH UNSAVED WARNING
================================= */
function goBack() {
    // Check if there are unsaved changes
    const saveButton = document.getElementById("saveButton");
    if (saveButton && saveButton.classList.contains("unsaved")) {
        if (!confirm("You have unsaved changes. Are you sure you want to leave?")) {
            return;
        }
    }
    
    window.location.href = `/voidships?fleet_id=${shipData.fleet_id}`;
}


/* ===============================
   AUTO LOAD ON PAGE OPEN
================================= */
document.addEventListener("DOMContentLoaded", () => {
    loadShipDetails();
    
    // Add event listeners for inputs
    const nameInput = document.getElementById("voidship_name");
    if (nameInput) {
        nameInput.addEventListener("input", updateTempData);
        nameInput.addEventListener("keypress", (event) => {
            if (event.key === "Enter") {
                saveShip();
            }
        });
    }
    
    // Add listeners for component changes that trigger recalculation
    // Example: when user changes plasma drive
    // document.getElementById("plasma_drive_select").addEventListener("change", () => {
    //     shipData.essential_plasma_drive = event.target.value;
    //     calculateStats();
    //     markAsUnsaved();
    // });
});