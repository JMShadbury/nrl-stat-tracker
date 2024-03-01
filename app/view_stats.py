from flask import Flask, render_template, request
from util.scoring import calculate_score
import json
from data_manager import load_data, load_rounds_data
from util.logger import configure_logger
import os


logger = configure_logger("flask.log")

app = Flask(__name__, static_folder=os.path.dirname(os.path.abspath(__file__)) + '/static')
team_data = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    logger.info("Index route called")
    try:
        teams = sorted(team_data.index.unique())
        selected_team1 = ''
        selected_team2 = ''
        comparison_data = None

        if request.method == 'POST':
            selected_team1 = request.form.get('team1', '')
            selected_team2 = request.form.get('team2', '')

            if selected_team1 in teams and selected_team2 in teams:
                team1_data = team_data.loc[selected_team1].to_dict()
                team2_data = team_data.loc[selected_team2].to_dict()

                team1_score = calculate_score(team1_data)
                team2_score = calculate_score(team2_data)

                comparison_data = {
                    'team1': {'name': selected_team1, 'data': team1_data, 'score': team1_score},
                    'team2': {'name': selected_team2, 'data': team2_data, 'score': team2_score}
                }

        return render_template('index.html', teams=teams, selected_team1=selected_team1, selected_team2=selected_team2, comparison_data=comparison_data)
    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        return "An error occurred", 500

    

@app.route('/ladder', methods=['GET'])
def view_ladder():
    '''
    Route to view the ladder
    '''
    logger.info("View ladder route called")
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
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return "An unexpected error occurred", 500
    
@app.route('/rounds')
def rounds():
    rounds_data = load_rounds_data()
    logger.debug("Rounds Data: {}".format(rounds_data))
    print(rounds_data)  # Use print to see the output directly in the console.
    return render_template('rounds.html', rounds=rounds_data)



if __name__ == '__main__':
    app.run(debug=True)