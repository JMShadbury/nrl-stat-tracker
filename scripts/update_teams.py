from util.dynamodb import DynamoDBClient
from util.data_processing import format_team_name_for_dynamodb
from teams.points import Points
from teams.tries import Tries
from teams.goals import Goals
import json
from util.logger import configure_logger

logger = configure_logger("UpdateTeams")
logger.setLevel("DEBUG")


logger.info("Updating teams data")
f = open("data/teams", "r")
team_names = f.read().splitlines()
f.close()

logger.debug(f"Teams: {team_names}")
team_names = {team.split(":")[0]: team.split(":")[1] for team in team_names}

tries_instance = Tries()
points_instance = Points()
goals_instance = Goals()

all_tries_data = tries_instance.get_all_tries_data()
all_points_data = points_instance.get_all_points_data()
all_goals_data = goals_instance.get_all_goals_data()


logger.info("Processing teams data")
for team_name in team_names:
    
    logger.info(f"Processing {team_name}")
    db_client = DynamoDBClient(team_name)


    tries_data = tries_instance.process_tries_data(all_tries_data, team_name)
    points_data = points_instance.process_points_data(all_points_data, team_name)
    goals_data = goals_instance.process_goals_data(all_goals_data, team_name)
    
    logger.debug(f"Tries data: {json.dumps(tries_data, indent=2)}")
    logger.debug(f"Points data: {json.dumps(points_data, indent=2)}")
    logger.debug(f"Goals data: {json.dumps(goals_data, indent=2)}")
    
    if tries_data['TeamName'] == points_data['TeamName'] == goals_data['TeamName'] == team_name:

        logger.info(f"Merging {team_name}")
        merged_data = tries_data.copy()  
        merged_data.update(points_data)
        
        logger.debug(f"Merged data: {json.dumps(merged_data, indent=2)}")
        
        logger.info(f"Inserting {team_name} into DynamoDB") 
        db_client.insert_item(merged_data)
