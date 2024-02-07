from flask import Flask, render_template, request, jsonify
import json
from data_manager import load_data
from util.logger import configure_logger


logger = configure_logger("flask.log")

app = Flask(__name__)
team_data = load_data()

@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    Index route for the web application
    '''
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
                # Extract data for the selected teams
                team1_data = team_data.loc[selected_team1].to_dict()
                team2_data = team_data.loc[selected_team2].to_dict()
                comparison_data = {'team1': {'name': selected_team1, 'data': team1_data},
                                   'team2': {'name': selected_team2, 'data': team2_data}}
            else:
                return "One or both teams not found.", 404
        else:
            selected_team1 = ''
            selected_team2 = ''
        logger.info(f"Selected teams: {selected_team1}, {selected_team2}")

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
        
        
    
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=80, debug=True)
