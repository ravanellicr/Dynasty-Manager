
document.addEventListener('DOMContentLoaded', function () {
    const dropdown = document.getElementById('hullSelect');

    fetch('///backend/data/hulls.json')
        .then(response => response.json())
        .then(data => {
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.value;
                option.textContent = item.text;
                dropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error loading the JSON:', error));
});