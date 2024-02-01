from util.dynamodb import DynamoDBClient
from util.data_processing import format_team_name_for_dynamodb
from teams.points import Points
from teams.tries import Tries


# Get Teams from file
f = open("data/teams", "r")
team_names = f.read().splitlines()
f.close()

team_names = {team.split(":")[0]: team.split(":")[1] for team in team_names}

tries_instance = Tries()
points_instance = Points()

# Scrape the data once
all_tries_data = tries_instance.get_all_tries_data()
all_points_data = points_instance.get_all_points_data()

for team_name in team_names:

    # Process data for each team
    tries_data = tries_instance.process_tries_data(all_tries_data, team_name)
    points_data = points_instance.process_points_data(all_points_data, team_name)

    # Insert data into DynamoDB
    if tries_data:
        points_tries_db_client.insert_item(tries_data)
    if points_data:
        points_tries_db_client.insert_item(points_data)
