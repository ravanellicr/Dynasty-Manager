let selectedDynasty = null;

async function loadDynastyList() {
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

async function newDynasty() {
  const name = prompt("New dynasty name:");
  if (!name) return;
  await apiPost(`/dynasties/create/${name}`);
  loadDynastyList();
}

async function copyDynasty() {
  if (!selectedDynasty) return alert("Select a dynasty first");
  await apiPost(`/dynasties/copy/${selectedDynasty}`);
  loadDynastyList();
}

async function deleteDynasty() {
  if (!selectedDynasty) return alert("Select a dynasty first");
  await fetch(`http://127.0.0.1:8000/dynasties/delete/${selectedDynasty}`, { method: "DELETE" });
  selectedDynasty = null;
  loadDynastyList();
}

async function loadDynasty() {
  if (!selectedDynasty) return alert("Select a dynasty first");

  await apiPost(`/dynasties/activate/${selectedDynasty}`);
  localStorage.setItem("activeDynasty", selectedDynasty);
  window.location.href = "dashboard.html";
}

loadDynastyList();
