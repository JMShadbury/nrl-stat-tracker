"""
Flask application
"""

# pylint: disable=C0301
# pylint: disable=C0303
# pylint: disable=E0401
# pylint: disable=W0718
# pylint: disable=W0621
# pylint: disable=C0413
# pylint: disable=C0411


import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.logger import configure_logger

from flask import Flask, render_template, request
from util.scoring import calculate_score, compare_teams
from data_manager import load_data, load_rounds_data


# Configure logger
logger = configure_logger("flask.log")

# Create Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
)

# Load team data
team_data = load_data()


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Route to compare teams.
    """
    logger.info("Index route called")
    try:
        teams = sorted(team_data.index.unique())
        selected_team1 = ""
        selected_team2 = ""
        comparison_data = None

        if request.method == "POST":
            selected_team1 = request.form.get("team1", "")
            selected_team2 = request.form.get("team2", "")

            if selected_team1 in teams and selected_team2 in teams:
                team1_data = team_data.loc[selected_team1].to_dict()
                team2_data = team_data.loc[selected_team2].to_dict()

                team1_score = calculate_score(team1_data)
                team2_score = calculate_score(team2_data)

                comparison_data = {
                    "team1": {
                        "name": selected_team1,
                        "data": team1_data,
                        "score": team1_score,
                    },
                    "team2": {
                        "name": selected_team2,
                        "data": team2_data,
                        "score": team2_score,
                    },
                }

        return render_template(
            "index.html",
            teams=teams,
            selected_team1=selected_team1,
            selected_team2=selected_team2,
            comparison_data=comparison_data,
        )
    except Exception as e:
        logger.error("Error processing request: %s", e, exc_info=True)
        return "An error occurred", 500


@app.route("/ladder", methods=["GET"])
def view_ladder():
    """
    Route to view the ladder.
    """
    logger.info("View ladder route called")
    try:
        with open("ladder/ladder_data.json", "r", encoding="utf-8") as file:
            ladder_data = json.load(file)
        return render_template("ladder.html", ladder_data=ladder_data)
    except FileNotFoundError:
        logger.error("Ladder data file not found.")
        return "Ladder data not found", 404
    except json.JSONDecodeError:
        logger.error("Error decoding ladder data file.")
        return "Error processing ladder data", 500
    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        return "An unexpected error occurred", 500


@app.route("/rounds")
def rounds():
    """
    Route to view the rounds.
    """
    rounds_data = load_rounds_data()
    logger.debug("Rounds Data: %s", rounds_data)
    print(rounds_data)  # Use print to see the output directly in the console.
    return render_template("rounds.html", rounds=rounds_data)


@app.route("/power_list")
def power_list():
    """
    Route to view the power list.
    """
    teams = sorted(team_data.index.unique())
    power_rankings = calculate_power_rankings(team_data, teams)
    return render_template("power_list.html", power_rankings=power_rankings)


def calculate_power_rankings(team_data, teams):
    """
    Calculate power rankings for the teams.

    Args:
        team_data (pd.DataFrame): DataFrame containing team data.
        teams (list): List of team names.

    Returns:
        list: List of dictionaries containing team rankings.
    """
    rankings = []
    predicted_wins = {
        team: [] for team in teams
    }  # Tracks predicted wins against specific teams

    for team in teams:
        wins = 0
        for opponent in teams:
            if team != opponent:
                winner = compare_teams(team_data, team, opponent)
                if winner == team:
                    wins += 1
                    predicted_wins[team].append(opponent)
        rankings.append(
            {"team": team, "wins": wins, "predicted_wins": predicted_wins[team]}
        )

    sorted_rankings = sorted(rankings, key=lambda x: x["wins"], reverse=True)

    for i, team_rank in enumerate(sorted_rankings):
        team_rank["defeats_higher_ranked"] = []
        for higher_team in sorted_rankings[:i]:
            if higher_team["team"] in team_rank["predicted_wins"]:
                team_rank["defeats_higher_ranked"].append(higher_team["team"])

    return sorted_rankings


if __name__ == "__main__":
    app.run(debug=True)
