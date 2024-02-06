from flask import Flask, render_template, request, Response, jsonify
import json
import base64
from io import BytesIO
from util.logger import configure_logger
from teams.data_manager import team_data
from teams.plotting import generate_comparison_plots, generate_all_plots
import threading, webbrowser

logger = configure_logger("flask.log")

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        teams = team_data.index.unique()  # Assuming team_data is a DataFrame with team names as index
        available_statistics = get_available_statistics()  # Your function to get available statistics
        images_data = []
        selected_team1 = ''
        selected_team2 = ''

        if request.method == 'POST':
            action = request.form.get('action')
            selected_team1 = request.form.get('team1', '')
            selected_team2 = request.form.get('team2', '')

            if action == 'compare':
                selected_statistic = request.form.get('statistic')

                if selected_team1 in teams and selected_team2 in teams:
                    images_data = generate_comparison_plots(team_data, selected_team1, selected_team2, [selected_statistic])
                else:
                    return "One or both teams not found.", 404
            elif action == 'all':
                # Call generate_all_plots function when 'Compare All' is selected
                images_data = generate_all_plots(team_data)

        return render_template('index.html', teams=teams, images_data=images_data,
                            available_statistics=available_statistics,
                            selected_team1=selected_team1,
                            selected_team2=selected_team2)
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return "An error occurred", 500



def get_unique_color_for_stat(stat, available_statistics):
    colors = [
        'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 
        'purple', 'pink', 'lime', 'orange', 'teal', 'coral', 'navy', 
        'maroon', 'olive', 'mint', 'apricot', 'beige', 'lavender'
    ]
    assert len(colors) >= len(available_statistics), "Not enough colors for the number of statistics"
    
    index = available_statistics.index(stat)
    
    return colors[index]

with open('data/Broncos.json', 'r') as json_file:
    data = json.load(json_file)

available_statistics = list(data[0].keys())


def get_available_statistics():
    with open('data/Broncos.json', 'r') as json_file:
        data = json.load(json_file)
    return list(data[0].keys())


@app.route('/stat/<statistic_name>')
def display_statistic(statistic_name):
    if statistic_name in team_data.columns:
        data = team_data[statistic_name]
        return render_template('statistic.html', data=data, statistic_name=statistic_name)
    else:
        return "Statistic not found", 404


@app.route('/plot', methods=['POST'])
def plot():
    team1 = request.form.get('team1')
    team2 = request.form.get('team2')
    selected_statistic = [request.form.get('statistic')]
    if team1 in team_data.index and team2 in team_data.index:
        images_data = generate_comparison_plots(team_data, team1, team2, [selected_statistic])
        return jsonify({'image_data': images_data})
    else:
        return jsonify({'error': 'One or both teams not found'}), 404
    
    
@app.route('/ladder', methods=['GET'])
def view_ladder():
    try:
        # Read ladder data from the JSON file
        with open('ladder/ladder_data.json', 'r') as file:
            ladder_data = json.load(file)
        return render_template('ladder.html', ladder_data=ladder_data)
    except FileNotFoundError:
        logger.error("Ladder data file not found.")
        return "Ladder data not found", 404
    except json.JSONDecodeError:
        logger.error("Error decoding ladder data file.")
        return "Error processing ladder data", 500

if __name__ == '__main__':

    port = 8000
    url = "http://127.0.0.1:{0}".format(port)

    threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

    app.run(port=port, debug=False)
