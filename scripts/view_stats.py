from flask import Flask, render_template, request, Response, jsonify
from teams.data_manager import team_data
from teams.plotting import generate_comparison_plots  # Import the function from plotting.py
import base64
from io import BytesIO
from logging.config import dictConfig
from util.logger import configure_logger

logger = configure_logger("flask.log")

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    images_data = []
    if request.method == 'POST':
        team1 = request.form.get('team1')
        team2 = request.form.get('team2')
        logger.info("Team 1: "+team1)
        logger.info("Team 2: "+team2)

        if team1 in team_data.index and team2 in team_data.index:
            logger.info(team1+" And "+team2+" found")  
            logger.info("Generating Data for "+team1+" And "+team2)
            
            # Use the generate_comparison_plots function from plotting.py
            images_data = generate_comparison_plots(team_data, team1, team2)
            
            logger.info("Data Generated for "+team1+" And "+team2)
        else:
            # Return a 404 status code when one or both teams are not found
            return ("One or both teams not found.", 404)

    logger.info("Rendering index.html {}".format(render_template('index.html', teams=team_data.index.unique(), images_data=images_data)))
    return render_template('index.html', teams=team_data.index.unique(), images_data=images_data)

@app.route('/plot', methods=['POST'])
def plot():
    team1 = request.form.get('team1')
    team2 = request.form.get('team2')
    if team1 in team_data.index and team2 in team_data.index:
        logger.info("Plotting Data for "+team1+" And "+team2)
        
        # Use the generate_comparison_plots function from plotting.py
        images_data = generate_comparison_plots(team_data, team1, team2)
        
        logger.info("Data Plotted for "+team1+" And "+team2)
        logger.info(jsonify({'image_data': images_data}))
        return jsonify({'image_data': images_data})
    else:
        # Return a 404 status code when one or both teams are not found
        return jsonify({'error': 'One or both teams not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
