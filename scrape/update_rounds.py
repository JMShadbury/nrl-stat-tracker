"""Module to update round data."""

# pylint: disable=E0401
# pylint: disable=C0303
# pylint: disable=W0622
# pylint: disable=C0413
# pylint: disable=R1705
# pylint: disable=C0103
# pylint: disable=W0718
# pylint: disable=C0103
# pylint: disable=W0718
# pylint: disable=C0411

from util.json_client import JSONClient
from util.defaults import Url
from stats.get_stats import Stats
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.logger import configure_logger

def append_with_comma(original, to_append):
    """Append a string with a comma."""
    if original:
        return original + "," + to_append
    else:
        return to_append

try:
    # Configure logger
    logger = configure_logger("UpdateRound.log")
    
    def create_stat_instance(url, stat_name):
        """Create an instance of the Stats class."""
        return Stats(url, stat_name)

    round_instances = {}

    count = 1
    while count <= 1:
        try:
            round_instances[count] = create_stat_instance(
                Url.get_draw_url(count), "Round: " + str(count))
            count += 1
        except Exception as e:
            logger.error(
                f"Error creating instance for Round {count}: {e}", exc_info=True)
            break

    logger.info("Initialization complete!")

    all_data = {round: instance.get_all_draw_data()
                for round, instance in round_instances.items()}

    try:
        logger.info("Processing All Round data")
        processed_data = {round: instance.process_draw_data(
            round, all_data[round]) for round, instance in round_instances.items()}
        logger.debug("Processed data: %s", processed_data)

    except Exception as e:
        logger.error("Error processing Round %s: %s", count, e, exc_info=True)

    # Define table schema
    table_name = 'NRL2024Rounds'

    # Create the table
    json_client = JSONClient(table_name)
    merged_data = {}

    for round, data in processed_data.items():
        if data:
            for d in data:
                current_game = create_stat_instance(
                    "https://www.nrl.com"+d['url'], "Game")
                all_current_game_data = current_game.get_all_game_data()
                processed_game_data = current_game.process_game_data(
                    all_current_game_data)
                merged_game_data = []
                for game in processed_game_data:
                    try:
                        match_info = {
                            'PreviousHomeTeams': game['PreviousHomeTeams'],
                            'PreviousAwayTeams': game['PreviousAwayTeams'],
                            'PreviousHomeScores': game['PreviousHomeScores'],
                            'PreviousAwayScores': game['PreviousAwayScores'],
                            'GamesPlayed': game['GamesPlayed'],
                            'AwayGamesWon': game['AwayGamesWon'],
                            'HomeGamesWon': game['HomeGamesWon']
                        }
                        merged_game_data.append(match_info)
                    except Exception as e:
                        logger.error(
                            "Error processing match data: %s", e, exc_info=True)

                logger.info(
                    "Processing %s - %s vs %s", round, d['HomeTeam'], d['AwayTeam'])

                home_team = d['HomeTeam']
                away_team = d['AwayTeam']
                stadium = d['Stadium']
                previous_home_teams = merged_game_data[0]['PreviousHomeTeams']
                previous_away_teams = merged_game_data[0]['PreviousAwayTeams']
                previous_home_scores = merged_game_data[0]['PreviousHomeScores']
                previous_away_scores = merged_game_data[0]['PreviousAwayScores']
                games_played = merged_game_data[0]['GamesPlayed']
                home_games_won = merged_game_data[0]['HomeGamesWon']
                away_games_won = merged_game_data[0]['AwayGamesWon']

                if round not in merged_data:
                    merged_data[round] = {
                        'Round': round,
                        'HomeTeams': home_team,
                        'AwayTeams': away_team,
                        'Stadiums': stadium,
                        'HomeGamesWon': home_games_won,
                        'AwayGamesWon': away_games_won,
                        'PreviousHomeScores': previous_home_scores,
                        'PreviousAwayScores': previous_away_scores,
                        'GamesPlayed': games_played,
                        'PreviousHomeTeams': previous_home_teams,
                        'PreviousAwayTeams': previous_away_teams
                    }
                else:
                    merged_data[round]['HomeTeams'] = append_with_comma(
                        merged_data[round]['HomeTeams'], home_team)
                    merged_data[round]['AwayTeams'] = append_with_comma(
                        merged_data[round]['AwayTeams'], away_team)
                    merged_data[round]['Stadiums'] = append_with_comma(
                        merged_data[round]['Stadiums'], stadium)
                    merged_data[round]['HomeGamesWon'] = append_with_comma(
                        merged_data[round]['HomeGamesWon'], home_games_won)
                    merged_data[round]['AwayGamesWon'] = append_with_comma(
                        merged_data[round]['AwayGamesWon'], away_games_won)
                    merged_data[round]['PreviousHomeScores'] = append_with_comma(
                        merged_data[round]['PreviousHomeScores'], previous_home_scores)
                    merged_data[round]['PreviousAwayScores'] = append_with_comma(
                        merged_data[round]['PreviousAwayScores'], previous_away_scores)
                    merged_data[round]['GamesPlayed'] = append_with_comma(
                        merged_data[round]['GamesPlayed'], games_played)
                    merged_data[round]['PreviousHomeTeams'] = append_with_comma(
                        merged_data[round]['PreviousHomeTeams'], previous_home_teams)
                    merged_data[round]['PreviousAwayTeams'] = append_with_comma(
                        merged_data[round]['PreviousAwayTeams'], previous_away_teams)
        else:
            logger.debug("No data found for Round %s", round)

    for round, data in merged_data.items():
        logger.info("Merged data for Round %s: %s", round, data)
        logger.info("Inserting Round %s into JSON", round)
        json_client.insert_item(data)
        logger.info("Round %s inserted into JSON", round)

except Exception as e:
    logger.error("An error occurred: %s", e, exc_info=True)
    raise e

logger.info("Scrape Successful!")
