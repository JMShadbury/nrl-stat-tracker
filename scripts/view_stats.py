from flask import Flask, render_template, request, Response, jsonify
import json
import base64
from io import BytesIO
from util.logger import configure_logger
from teams.data_manager import team_data
from teams.plotting import generate_comparison_plots

logger = configure_logger("flask.log")

app = Flask(__name__)

# Read the JSON data from the file or your data source
with open('data/Broncos.json', 'r') as json_file:
    data = json.load(json_file)

# Extract the statistics (keys) from the JSON data
available_statistics = list(data[0].keys())

@app.route('/', methods=['GET', 'POST'])
def index():
    images_data = []
    teams = team_data.index.unique()  # Get the list of teams
    if request.method == 'POST':
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')
        selected_statistic = request.form.get('statistic')  # Get the selected statistic
        print(selected_statistic)

        if team1 in teams and team2 in teams:
            images_data = generate_comparison_plots(team_data, team1, team2, [selected_statistic])  # Pass the selected statistic as a list
        else:
            return ("One or both teams not found.", 404)

    # Get available statistics dynamically
    available_statistics = get_available_statistics()

    return render_template('index.html', teams=teams, images_data=images_data, available_statistics=available_statistics)  # Pass available_statistics to the template





def get_available_statistics():
    # Define a list of available statistics
    available_stats = [
        "Support",
        "Try Assists",
        "Kick Return Metres",
        "Tackle Breaks",
        "Line Engaged",
        "Kick Metres",
        "Conversion Percentage",
        "Completion",
        "Kicks",
        "Post Contact Metres",
        "Offloads",
        "Goals",
        "Line Breaks",
        "Tries",
        "Points",
        "Line Break Assists",
        "Runs",
        "Played",
        "Run Metres"
    ]
    return available_stats


@app.route('/stat/<statistic_name>')
def display_statistic(statistic_name):
    if statistic_name in team_data.columns:
        # Get data for the selected statistic
        data = team_data[statistic_name]
        return render_template('statistic.html', data=data, statistic_name=statistic_name)
    else:
        return "Statistic not found", 404


@app.route('/plot', methods=['POST'])
def plot():
    team1 = request.form.get('team1')
    team2 = request.form.get('team2')
    selected_statistic = [request.form.get('statistic')]  # Pass the selected statistic as a list
    if team1 in team_data.index and team2 in team_data.index:
        # Use the generate_comparison_plots function from plotting.py
        images_data = generate_comparison_plots(team_data, team1, team2, selected_statistic)
        return jsonify({'image_data': images_data})
    else:
        return jsonify({'error': 'One or both teams not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)
