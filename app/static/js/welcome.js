function openStats(team) {
    const teamName = team.replace(".svg", "")
    fetch(`/team_stats/${encodeURIComponent(teamName)}`)
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        updateModalContent(data, teamName);
        displayModal();
    })
    .catch(error => {
        console.error('Error fetching team stats:', error);
    });
}

function updateModalContent(data, teamName) {
    const modalContent = document.querySelector('.modal-content');
    const teamNameElement = modalContent.querySelector('#team-name');
    teamNameElement.textContent = teamName; // Set the team name

    console.log("team name: ", teamName);
    console.log("data: ", data);

    // Clear previous stats
    const existingTable = modalContent.querySelector('table');
    if (existingTable) existingTable.remove();

    // Create a new table for stats
    const table = document.createElement('table');
    Object.entries(data).forEach(([stat, value]) => {
        const row = table.insertRow();
        const statCell = row.insertCell();
        const valueCell = row.insertCell();
        statCell.textContent = stat;
        valueCell.textContent = value;
    });
    modalContent.appendChild(table); // Append the table to the modal content
}

function displayModal() {
    const modal = document.getElementById('stats-modal');
    modal.style.display = 'block';
}

// Add event listener for closing the modal
const closeSpan = document.querySelector('.modal-content .close');
closeSpan.onclick = function() {
    document.getElementById('stats-modal').style.display = 'none';
};
