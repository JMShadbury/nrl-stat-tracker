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
    completion_instance = Stats(Url.TEAM_COMPLETION.value, "Completion")
    support_instance = Stats(Url.TEAM_SUPPORT.value, "Support")
    line_breaks_instance = Stats(Url.TEAM_LINE_BREAKS.value, "Line Breaks")
    post_contact_metres_instance = Stats(
        Url.TEAM_POST_CONTACT_METRES.value, "Post Contact Metres")
    tackle_breaks_instance = Stats(Url.TEAM_TACKLE_BREAKS.value, "Tackle Breaks")
    run_metres_instance = Stats(Url.TEAM_ALL_RUN_METRES.value, "Run Metres")
    runs_instance = Stats(Url.TEAM_ALL_RUNS.value, "Runs")
    kick_return_metres_instance = Stats(
        Url.TEAM_KICK_RETURN_METRES.value, "Kick Return Metres")
    offloads_instance = Stats(Url.TEAM_OFFLOADS.value, "Offloads")
    line_break_assists_instance = Stats(
        Url.TEAM_LINE_BREAK_ASSISTS
        .value, "Line Break Assists")
    kicks_instance = Stats(Url.TEAM_TOTAL_KICKS.value, "Kicks")
    kick_metres_instance = Stats(Url.TEAM_TOTAL_KICK_METRES.value, "Kick Metres")
    try_assists_instance = Stats(Url.TEAM_TRY_ASSISTS.value, "Try Assists")
    conversion_percentage_instance = Stats(
        Url.TEAM_CONVERSION_PERCENT.value, "Conversion Percentage")
    

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
    all_completion_data = completion_instance.get_all_data()
    all_support_data = support_instance.get_all_data()
    all_line_breaks_data = line_breaks_instance.get_all_data()
    all_post_contact_metres_data = post_contact_metres_instance.get_all_data()
    all_tackle_breaks_data = tackle_breaks_instance.get_all_data()
    all_run_metres_data = run_metres_instance.get_all_data()
    all_runs_data = runs_instance.get_all_data()
    all_kick_return_metres_data = kick_return_metres_instance.get_all_data()
    all_offloads_data = offloads_instance.get_all_data()
    all_line_break_assists_data = line_break_assists_instance.get_all_data()
    all_kicks_data = kicks_instance.get_all_data()
    all_kick_metres_data = kick_metres_instance.get_all_data()
    all_try_assists_data = try_assists_instance.get_all_data()
    all_conversion_percentage_data = conversion_percentage_instance.get_all_data()
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
        completion_data = completion_instance.process_data(
            all_completion_data, team_name)
        support_data = support_instance.process_data(
            all_support_data, team_name)
        line_breaks_data = line_breaks_instance.process_data(
            all_line_breaks_data, team_name)
        post_contact_metres_data = post_contact_metres_instance.process_data(
            all_post_contact_metres_data, team_name)
        tackle_breaks_data = tackle_breaks_instance.process_data(
            all_tackle_breaks_data, team_name)
        run_metres_data = run_metres_instance.process_data(
            all_run_metres_data, team_name)
        runs_data = runs_instance.process_data(all_runs_data, team_name)
        kick_return_metres_data = kick_return_metres_instance.process_data(
            all_kick_return_metres_data, team_name)
        offloads_data = offloads_instance.process_data(
            all_offloads_data, team_name)
        line_break_assists_data = line_break_assists_instance.process_data(
            all_line_break_assists_data, team_name)
        kicks_data = kicks_instance.process_data(all_kicks_data, team_name)
        kick_metres_data = kick_metres_instance.process_data(
            all_kick_metres_data, team_name)
        try_assists_data = try_assists_instance.process_data(
            all_try_assists_data, team_name)
        conversion_percentage_data = conversion_percentage_instance.process_data(
            all_conversion_percentage_data, team_name)
        logger.warning(f"Tries data: {json.dumps(tries_data, indent=2)}")
        logger.warning(f"Points data: {json.dumps(points_data, indent=2)}")
        logger.warning(f"Goals data: {json.dumps(goals_data, indent=2)}")
        logger.warning(
            f"Line Engaged data: {json.dumps(line_engaged_data, indent=2)}")
        logger.warning(
            f"Completion data: {json.dumps(completion_data, indent=2)}")
        logger.warning(
            f"Support data: {json.dumps(support_data, indent=2)}")
        logger.warning(
            f"Line Breaks data: {json.dumps(line_breaks_data, indent=2)}")
        logger.warning(
            f"Post Contact Metres data: {json.dumps(post_contact_metres_data, indent=2)}")
        logger.warning(
            f"Tackle Breaks data: {json.dumps(tackle_breaks_data, indent=2)}")
        logger.warning(
            f"Run Metres data: {json.dumps(run_metres_data, indent=2)}")
        logger.warning(
            f"Runs data: {json.dumps(runs_data, indent=2)}")
        logger.warning(
            f"Kick Return Metres data: {json.dumps(kick_return_metres_data, indent=2)}")
        logger.warning(
            f"Offloads data: {json.dumps(offloads_data, indent=2)}")
        logger.warning(
            f"Line Break Assists data: {json.dumps(line_break_assists_data, indent=2)}")
        logger.warning(
            f"Kicks data: {json.dumps(kicks_data, indent=2)}")
        logger.warning(
            f"Kick Metres data: {json.dumps(kick_metres_data, indent=2)}")
        logger.warning(
            f"Try Assists data: {json.dumps(try_assists_data, indent=2)}")
        logger.warning(
            f"Conversion Percentage data: {json.dumps(conversion_percentage_data, indent=2)}")
        

        if (
            tries_data['TeamName'].replace(" ", "") ==
            points_data['TeamName'].replace(" ", "") ==
            goals_data['TeamName'].replace(" ", "") ==
            line_engaged_data['TeamName'].replace(" ", "") ==
            completion_data['TeamName'].replace(" ", "") ==
            support_data['TeamName'].replace(" ", "") ==
            line_breaks_data['TeamName'].replace(" ", "") ==
            post_contact_metres_data['TeamName'].replace(" ", "") ==
            tackle_breaks_data['TeamName'].replace(" ", "") ==
            run_metres_data['TeamName'].replace(" ", "") ==
            runs_data['TeamName'].replace(" ", "") ==
            kick_return_metres_data['TeamName'].replace(" ", "") ==
            offloads_data['TeamName'].replace(" ", "") ==
            line_break_assists_data['TeamName'].replace(" ", "") ==
            kicks_data['TeamName'].replace(" ", "") ==
            kick_metres_data['TeamName'].replace(" ", "") ==
            try_assists_data['TeamName'].replace(" ", "") ==
            conversion_percentage_data['TeamName'].replace(" ", "") ==
            team_name.replace(" ", "")
        ):

            logger.info(f"Merging {team_name}")
            merged_data = tries_data.copy()
            merged_data.update(points_data)
            merged_data.update(goals_data)
            merged_data.update(line_engaged_data)
            merged_data.update(completion_data)
            merged_data.update(support_data)
            merged_data.update(line_breaks_data)
            merged_data.update(post_contact_metres_data)
            merged_data.update(tackle_breaks_data)
            merged_data.update(run_metres_data)
            merged_data.update(runs_data)
            merged_data.update(kick_return_metres_data)
            merged_data.update(offloads_data)
            merged_data.update(line_break_assists_data)
            merged_data.update(kicks_data)
            merged_data.update(kick_metres_data)
            merged_data.update(try_assists_data)
            merged_data.update(conversion_percentage_data)
            logger.debug(f"Merged data: {json.dumps(merged_data, indent=2)}")
            logger.info(f"Inserting {team_name} into DynamoDB")
            if merged_data:
                db_client.insert_item(merged_data)
            continue
    except Exception as e:
        logger.error(f"Error processing {team_name}: {e}", exc_info=True)
        raise e
