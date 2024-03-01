document.addEventListener('DOMContentLoaded', (event) => {
    const team1Select = document.querySelector('select[name="team1"]');
    const team2Select = document.querySelector('select[name="team2"]');

    function handleTeamSelect(event) {
        // Get the selected values
        const selectedTeam1 = team1Select.value;
        const selectedTeam2 = team2Select.value;

        // Enable all options
        Array.from(team1Select.options).forEach(option => option.disabled = false);
        Array.from(team2Select.options).forEach(option => option.disabled = false);

        // Disable the selected options in the opposite select
        if (selectedTeam1) team2Select.querySelector(`option[value="${selectedTeam1}"]`).disabled = true;
        if (selectedTeam2) team1Select.querySelector(`option[value="${selectedTeam2}"]`).disabled = true;
    }

    // Add event listeners
    team1Select.addEventListener('change', handleTeamSelect);
    team2Select.addEventListener('change', handleTeamSelect);

    // Initial call to set the correct disabled state
    handleTeamSelect();
});

function searchStats() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("statsSearch");
    filter = input.value.toUpperCase();
    table = document.getElementById("statsTable");
    tr = table.getElementsByTagName("tr");

    for (i = 0; i < tr.length; i++) {
        td = tr[i].getElementsByTagName("td")[0];
        if (td) {
            txtValue = td.textContent || td.innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
                tr[i].style.display = "";
            } else {
                tr[i].style.display = "none";
            }
        }
    }
}

function updateScoreBar(team1Name, team1Score, team2Name, team2Score, team1IconUrl, team2IconUrl) {
    // Calculate percentages and determine winning team and icon
    const totalScore = parseFloat(team1Score) + parseFloat(team2Score);
    const team1Percentage = (parseFloat(team1Score) / totalScore) * 100;
    const team2Percentage = (parseFloat(team2Score) / totalScore) * 100;
    const winningIcon = parseFloat(team1Score) > parseFloat(team2Score) ? team1IconUrl : team2IconUrl;
    const winningPercentage = Math.max(team1Percentage, team2Percentage).toFixed(2);

    // Update elements
    document.getElementById('team1-bar').style.width = `${team1Percentage}%`;
    document.getElementById('team2-bar').style.width = `${team2Percentage}%`;
    const winningTeamIconElement = document.getElementById('winning-team-icon');
    winningTeamIconElement.src = winningIcon;
    winningTeamIconElement.style.display = 'block';
    document.getElementById('winning-percentage').textContent = `${winningPercentage}%`;
}

document.addEventListener('DOMContentLoaded', () => {
    const team1Select = document.querySelector('select[name="team1"]');
    const team2Select = document.querySelector('select[name="team2"]');

    function handleTeamSelect() {
        const selectedTeam1 = team1Select.value;
        const selectedTeam2 = team2Select.value;

        if (selectedTeam1 && selectedTeam2) {
            const team1Data = comparison_data.team1;
            const team2Data = comparison_data.team2;

            // Get the score values
            const team1Score = parseFloat(team1Data.score);
            const team2Score = parseFloat(team2Data.score);

            // Extract icon URLs from the existing <img> tags
            const team1IconUrl = document.querySelector('img[alt="' + team1Data.name + '"]').src;
            const team2IconUrl = document.querySelector('img[alt="' + team2Data.name + '"]').src;

            updateScoreBar(team1Data.name, team1Score, team2Data.name, team2Score, team1IconUrl, team2IconUrl);
        }
    }

    // Add event listeners
    team1Select.addEventListener('change', handleTeamSelect);
    team2Select.addEventListener('change', handleTeamSelect);

    // Initial call to set the correct disabled state and update the score bar
    handleTeamSelect();
});