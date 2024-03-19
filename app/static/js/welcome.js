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
    
    // Find and remove the existing team icon if present
    const existingTeamIcon = modalContent.querySelector('.team-icon');
    if (existingTeamIcon) {
        existingTeamIcon.remove();
    }

    // Capitalize the first letter of the team name and keep the rest in lower case
    const formattedTeamName = teamName.charAt(0).toUpperCase() + teamName.slice(1).toLowerCase();

    // Create and insert new team icon
    const teamIcon = document.createElement('img');
    teamIcon.src = '/static/img/' + formattedTeamName + '.svg'; // Adjust the path for Flask app structure
    teamIcon.alt = teamName;
    teamIcon.className = 'team-icon';
    modalContent.insertBefore(teamIcon, modalContent.firstChild); // Insert the icon at the beginning

    // Clear previous stats
    const existingTable = modalContent.querySelector('table');
    if (existingTable) existingTable.remove();

    // Create a new table for stats
    const table = document.createElement('table');

    
    const statsOrder = [
        "Played",
        "Tries",
        "Try Assists",
        "Points",
        "Goals",
        "Line Breaks",
        "Line Break Assists",
        "Completion",
        "Possession",
        "Conversion Percentage",
        "Offloads",
        "Tackle Breaks",
        "Post Contact Metres",
        "Kick Metres",
        "Dummy Half Runs",
        "Support",
        "Runs",
        "Run Metres",
        "Kicks",
        "Kick Return Metres",
        "Tackles",
        "Missed Tackles",
        "Ineffective Tackles",
        "Errors",
        "Handling Errors",
        "Penalties Conceded",
        "Intercepts",
        "Line Engaged",
        "All Receipts",
        "Decoy Runs",
        "Charge Downs",
    ];

    // Iterate over statsOrder to ensure stats are displayed in the desired order
    statsOrder.forEach(stat => {
        if (data.hasOwnProperty(stat)) {
            const row = table.insertRow();
            const statCell = row.insertCell();
            const valueCell = row.insertCell();
            statCell.textContent = stat;
            valueCell.textContent = data[stat];
        }
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
