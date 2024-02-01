from util.dynamodb import DynamoDBClient
from util.data_processing import format_team_name_for_dynamodb
from teams.points import Points
from teams.tries import Tries


# Get Teams from file
f = open("data/teams", "r")
team_names = f.read().splitlines()
f.close()

team_names = {team.split(":")[0]: team.split(":")[1] for team in team_names}

for team_name in team_names:
    print(team_name)
    formatted_table_name = format_team_name_for_dynamodb(team_name)
    points_tries_db_client = DynamoDBClient(formatted_table_name)

    # Here, you would call your methods to scrape tries and points data
    # For example: 
    tries_data = Tries.get_tries_data_for_team(team_name)
    points_data = Points.get_points_data_for_team(team_name)

    points_tries_db_client.insert_item(tries_data)
    points_tries_db_client.insert_item(points_data)