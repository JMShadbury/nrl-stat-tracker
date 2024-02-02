import json
from util.dynamodb import DynamoDBClient
from util.data_processing import format_team_name_for_dynamodb
from util.defaults import Url
from teams.stats import Stats
from util.logger import configure_logger

try:
    logger = configure_logger("UpdateTeams")
    logger.setLevel("DEBUG")

    # Stats
    tries_instance = Stats(Url.TEAM_TRIES.value, "Tries")
    points_instance = Stats(Url.TEAM_POINTS.value, "Points")
    goals_instance = Stats(Url.TEAM_GOALS.value, "Goals")
    line_engaged_instance = Stats(Url.TEAM_LINE_ENGAGED.value, "Line Engaged")

    logger.info("Updating teams data")
    f = open("data/teams", "r")
    team_names = f.read().splitlines()
    f.close()

    logger.debug(f"Teams: {team_names}")
    team_names = {team.split(":")[0]: team.split(":")[1]
                  for team in team_names}

    all_tries_data = tries_instance.get_all_data()
    all_points_data = points_instance.get_all_data()
    all_goals_data = goals_instance.get_all_data()
    all_line_engaged_data = line_engaged_instance.get_all_data()

    logger.info("Processing teams data")

except Exception as e:
    logger.error(f"Error updating teams data: {e}", exc_info=True)
    raise e

for team_name in team_names:
    try:
        logger.info(f"Processing {team_name}")
        db_client = DynamoDBClient(team_name)
        tries_data = tries_instance.process_data(all_tries_data, team_name)
        points_data = points_instance.process_data(
            all_points_data, team_name)
        goals_data = goals_instance.process_data(all_goals_data, team_name)
        line_engaged_data = line_engaged_instance.process_data(
            all_line_engaged_data, team_name)
        logger.warning(f"Tries data: {json.dumps(tries_data, indent=2)}")
        logger.warning(f"Points data: {json.dumps(points_data, indent=2)}")
        logger.warning(f"Goals data: {json.dumps(goals_data, indent=2)}")
        logger.warning(
            f"Line Engaged data: {json.dumps(line_engaged_data, indent=2)}")

        if (
            tries_data['TeamName'].replace(" ", "") ==
            points_data['TeamName'].replace(" ", "") ==
            goals_data['TeamName'].replace(" ", "") ==
            line_engaged_data['TeamName'].replace(" ", "") ==
            team_name.replace(" ", "")
        ):

            logger.info(f"Merging {team_name}")
            merged_data = tries_data.copy()
            merged_data.update(points_data)
            merged_data.update(goals_data)
            merged_data.update(line_engaged_data)
            logger.debug(f"Merged data: {json.dumps(merged_data, indent=2)}")
            logger.info(f"Inserting {team_name} into DynamoDB")
            db_client.insert_item(merged_data)
            continue
    except Exception as e:
        logger.error(f"Error processing {team_name}: {e}", exc_info=True)
        raise e
