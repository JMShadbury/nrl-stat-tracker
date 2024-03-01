import json
from util.json_client import JSONClient
from util.defaults import Url
from stats.get_stats import Stats
from util.logger import configure_logger

try:
    logger = configure_logger("UpdateTeams.log")
    logger.setLevel("DEBUG")

    def create_stat_instance(url, stat_name):
        return Stats(url.value, stat_name)

    stats_instances = {
        "Tries": create_stat_instance(Url.TEAM_TRIES, "Tries"),
        "Points": create_stat_instance(Url.TEAM_POINTS, "Points"),
        "Goals": create_stat_instance(Url.TEAM_GOALS, "Goals"),
        "Line Engaged": create_stat_instance(Url.TEAM_LINE_ENGAGED, "Line Engaged"),
        "Completion": create_stat_instance(Url.TEAM_COMPLETION, "Completion"),
        "Support": create_stat_instance(Url.TEAM_SUPPORT, "Support"),
        "Line Breaks": create_stat_instance(Url.TEAM_LINE_BREAKS, "Line Breaks"),
        "Post Contact Metres": create_stat_instance(Url.TEAM_POST_CONTACT_METRES, "Post Contact Metres"),
        "Tackle Breaks": create_stat_instance(Url.TEAM_TACKLE_BREAKS, "Tackle Breaks"),
        "Run Metres": create_stat_instance(Url.TEAM_ALL_RUN_METRES, "Run Metres"),
        "Runs": create_stat_instance(Url.TEAM_ALL_RUNS, "Runs"),
        "Kick Return Metres": create_stat_instance(Url.TEAM_KICK_RETURN_METRES, "Kick Return Metres"),
        "Offloads": create_stat_instance(Url.TEAM_OFFLOADS, "Offloads"),
        "Line Break Assists": create_stat_instance(Url.TEAM_LINE_BREAK_ASSISTS, "Line Break Assists"),
        "Kicks": create_stat_instance(Url.TEAM_TOTAL_KICKS, "Kicks"),
        "Kick Metres": create_stat_instance(Url.TEAM_TOTAL_KICK_METRES, "Kick Metres"),
        "Try Assists": create_stat_instance(Url.TEAM_TRY_ASSISTS, "Try Assists"),
        "Conversion Percentage": create_stat_instance(Url.TEAM_CONVERSION_PERCENT, "Conversion Percentage"),
        "All Receipts": create_stat_instance(Url.TEAM_ALL_RECEIPTS, "All Receipts"),
        "Field Goals": create_stat_instance(Url.TEAM_FIELD_GOALS, "Field Goals"),
        "Decoy Runs": create_stat_instance(Url.TEAM_DECOY_RUNS, "Decoy Runs"),
        "Dummy Half Runs": create_stat_instance(Url.TEAM_DUMMY_HALF_RUNS, "Dummy Half Runs"),
        "Tackles": create_stat_instance(Url.TEAM_TACKLES, "Tackles"),
        "Missed Tackles": create_stat_instance(Url.TEAM_MISSED_TACKLES, "Missed Tackles"),
        "Charge Downs": create_stat_instance(Url.TEAM_CHARGE_DOWNS, "Charge Downs"),
        "Intercepts": create_stat_instance(Url.TEAM_INTERCEPTS, "Intercepts"),
        "40/20 Kicks": create_stat_instance(Url.TEAM_40_20_KICKS, "40/20 Kicks"),
        "Short Dropouts": create_stat_instance(Url.TEAM_SHORT_DROPOUTS, "Short Dropouts"),
        "Errors": create_stat_instance(Url.TEAM_ERRORS, "Errors"),
        "Ineffective Tackles": create_stat_instance(Url.TEAM_INEFFECTIVE_TACKLES, "Ineffective Tackles"),
        "Penalties Conceded": create_stat_instance(Url.TEAM_PENALTIES_CONCEDED, "Penalties Conceded"),
        "Handling Errors": create_stat_instance(Url.TEAM_HANDLING_ERRORS, "Handling Errors")
    }

    logger.info("Updating teams data")
    with open("app/teams/teams", "r") as f:
        team_names = f.read().splitlines()

    logger.debug(f"Teams: {team_names}")
    team_names = {team.split(":")[0]: team.split(":")[1]
                  for team in team_names}
    all_data = {stat_name: instance.get_all_teams_data()
                for stat_name, instance in stats_instances.items()}
    logger.info("Processing teams data")

    for team_name in team_names:
        try:
            logger.info(f"Processing {team_name}")
            db_client = JSONClient(team_name)

            processed_data = {stat_name: instance.process_teams_data(
                all_data[stat_name], team_name) for stat_name, instance in stats_instances.items()}
            if all(
                team_name.replace(" ", "") == (data['TeamName'].replace(
                    " ", "") if data and 'TeamName' in data else "")
                for data in processed_data.values() if data and 'TeamName' in data
            ):

                # Filter out None values from processed_data
                filtered_processed_data = {
                    k: v for k, v in processed_data.items() if v is not None}

                # Create the merged_data dictionary
                merged_data = {key: value for d in filtered_processed_data.values()
                               for key, value in d.items()}

                logger.info(
                    f"Merged data for {team_name}: {json.dumps(merged_data, indent=2)}")
                if merged_data:
                    logger.info(f"Inserting {team_name} into JSON")
                    db_client.insert_item(merged_data)
                else:
                    logger.debug(f"No data found for {team_name}")
            else:
                logger.debug(f"Team name mismatch for {team_name}")
        except Exception as e:
            logger.error(f"Error processing {team_name}: {e}", exc_info=True)
except Exception as e:
    logger.error(f"An error occurred: {e}")
    raise e
