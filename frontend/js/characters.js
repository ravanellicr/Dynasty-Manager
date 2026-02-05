async function createCharacter() {
  const character = {
    name: document.getElementById("name").value,
    homeworld: document.getElementById("homeworld").value,
    career: document.getElementById("career").value
  };

  await apiPost("/characters/", character);
  loadCharacters();
}

async function loadCharacters() {
  const chars = await apiGet("/characters/");
  const list = document.getElementById("charList");
  list.innerHTML = "";

  chars.forEach(c => {
    const li = document.createElement("li");
    li.textContent = `${c.name} — ${c.career}`;
    list.appendChild(li);
  });
}

loadCharacters();
