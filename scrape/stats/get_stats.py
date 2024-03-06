""" This module contains functionality for scraping statistics from the NRL website. """

# pylint: disable=E0401
# pylint: disable=E1126
# pylint: disable=C0301
# pylint: disable=C0413
# pylint: disable=C0116
# pylint: disable=R1705
# pylint: disable=C0115
# pylint: disable=C0209
# pylint: disable=R0914
# pylint: disable=W0702
# pylint: disable=W0718
# pylint: disable=C0209
# pylint: disable=E1126
# pylint: disable=R0915
# pylint: disable=W0622
# pylint: disable=W0613
# pylint: disable=C0411

from util.scraper import WebScraper
from stats.constants import TeamDefaults, RoundDefaults, GameDefaults
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from common.logger import get_logger

logger = get_logger()


def process_table_row(row, stat):
    """
    Process a table row
    :param row: The table row to process
    :param stat: The statistic to process
    :return: The processed data
    """
    played = row.select_one('td:nth-of-type(4)').get_text(strip=True)
    goals = row.select_one('td:nth-of-type(5)').get_text(strip=True)

    data = {
        'TeamName': row.select_one('span.u-font-weight-600').get_text(strip=True),
        'Played': played,
        stat: goals
    }
    return data


def append_with_comma(original, to_append):
    if original:
        return original + "," + to_append
    else:
        return to_append


class Stats:

    def __init__(self, url, stat):
        '''
        Initialise the Stats class
        :param url: The URL to scrape
        :param stat: The statistic to scrape
        '''
        logger.info("Initialising {}".format(stat))
        logger.debug("URL: {}".format(url))
        self.url = url
        self.stat = stat
        self.scraper = WebScraper(self.url)

    def get_all_game_data(self):
        '''
        Get all the data from the URL
        :return: The data from the URL
        '''
        logger.info("Getting data for {}".format(self.stat))
        return self.scraper.load_page(GameDefaults.GAME_PATH.value)

    def get_all_draw_data(self):
        '''
        Get all the data from the URL
        :return: The data from the URL
        '''
        logger.info("Getting data for {}".format(self.stat))
        return self.scraper.load_page(RoundDefaults.MATCH_PATH.value)

    def get_all_teams_data(self):
        '''
        Get all the data from the URL
        :return: The data from the URL
        '''
        return self.scraper.load_page(TeamDefaults.TEAMS_PATH.value)

    def process_game_data(self, soup):
        '''
        Process the data
        :param soup: The data to process
        :return: The processed data
        '''

        def get_home_score(data):
            try:
                home_score = data.find(
                    GameDefaults.GAME_PREV_HOME_SCORE_TAG.value, class_=GameDefaults.GAME_PREV_HOME_SCORE_CLASS.value).text.strip()
            except:
                home_score = data.find(
                    GameDefaults.GAME_PREV_HOME_SCORE_TAG.value, class_=GameDefaults.GAME_PREV_HOME_SCORE_CLASS.value+GameDefaults.GAME_PREV_SCORE_WINNER_CLASS.value).text.strip()
            home_score = home_score.replace(" ", "").strip(
                "Scored").strip("points").strip("\n")
            return home_score

        def get_away_score(data):
            try:
                away_score = data.find(
                    GameDefaults.GAME_PREV_AWAY_SCORE_TAG.value, class_=GameDefaults.GAME_PREV_AWAY_SCORE_CLASS.value).text.strip()
            except:
                away_score = data.find(
                    GameDefaults.GAME_PREV_AWAY_SCORE_TAG.value, class_=GameDefaults.GAME_PREV_AWAY_SCORE_CLASS.value+GameDefaults.GAME_PREV_SCORE_WINNER_CLASS.value).text.strip()
            away_score = away_score.replace(" ", "").strip(
                "Scored").strip("points").strip("\n")
            return away_score

        def get_games_played(data):
            try:
                games_played = data.find(
                    GameDefaults.GAME_PLAYED_TAG.value, class_=GameDefaults.GAME_PLAYED_CLASS.value).text.strip()
            except Exception as e:
                logger.error(
                    "Error processing game data: {}".format(e), exc_info=True)
            return games_played

        def get_home_games_won(data):
            games_won = 0
            try:
                games_won = data.find(
                    GameDefaults.GAME_HOME_WINS_TAG.value, class_=GameDefaults.GAME_HOME_WINS_CLASS.value).text.strip()
            except:
                games_won = data.find(
                    GameDefaults.GAME_HOME_WINS_TAG.value, class_=GameDefaults.GAME_HOME_WINS_CLASS.value+GameDefaults.GAME_WINS_WINNER_CLASS.value).text.strip()
            return games_won

        def get_away_games_won(data):
            games_won = 0
            try:
                games_won = data.find(
                    GameDefaults.GAME_AWAY_WINS_TAG.value, class_=GameDefaults.GAME_AWAY_WINS_CLASS.value).text.strip()
            except:
                games_won = data.find(
                    GameDefaults.GAME_AWAY_WINS_TAG.value, class_=GameDefaults.GAME_AWAY_WINS_CLASS.value+GameDefaults.GAME_WINS_WINNER_CLASS.value).text.strip()
            return games_won

        def get_home_name(data):
            home_name = data.find(
                GameDefaults.GAME_PREV_HOME_NAME_TAG.value, class_=GameDefaults.GAME_PREV_HOME_NAME_CLASS.value).text.strip()
            return home_name

        def get_away_name(data):
            away_name = data.find(
                GameDefaults.GAME_PREV_AWAY_NAME_TAG.value, class_=GameDefaults.GAME_PREV_AWAY_NAME_CLASS.value).text.strip()
            return away_name

        if soup:
            game_previous_containers = soup.find_all(
                GameDefaults.GAME_PREV_CONTAINER_TAG.value, class_=GameDefaults.GAME_PREV_CONTAINER_CLASS.value)
            game_previous_data = []
            match_data = []

            for game in game_previous_containers:
                try:
                    home_score = get_home_score(game)
                    away_score = get_away_score(game)
                    home_name = get_home_name(game)
                    away_name = get_away_name(game)

                    if game_previous_data:
                        game_previous_data['PreviousHomeScore'] = append_with_comma(
                            game_previous_data['PreviousHomeScore'], home_score)
                        game_previous_data['PreviousAwayScore'] = append_with_comma(
                            game_previous_data['PreviousAwayScore'], away_score)
                        game_previous_data['PreviousHomeTeam'] = append_with_comma(
                            game_previous_data['PreviousHomeTeam'], home_name)
                        game_previous_data['PreviousAwayTeam'] = append_with_comma(
                            game_previous_data['PreviousAwayTeam'], away_name)
                    else:
                        game_previous_data = {
                            'PreviousHomeScore': home_score,
                            'PreviousAwayScore': away_score,
                            'PreviousHomeTeam': home_name,
                            'PreviousAwayTeam': away_name
                        }

                except Exception as e:
                    logger.error(
                        "Error processing game data: {}".format(e), exc_info=True)
            try:
                logger.info("Preparing match data")
                match_info = {
                    'PreviousHomeTeams': game_previous_data['PreviousHomeTeam'],
                    'PreviousAwayTeams': game_previous_data['PreviousAwayTeam'],
                    'PreviousHomeScores': game_previous_data['PreviousHomeScore'],
                    'PreviousAwayScores': game_previous_data['PreviousAwayScore'],
                    'GamesPlayed': get_games_played(soup),
                    'AwayGamesWon': get_away_games_won(soup),
                    'HomeGamesWon': get_home_games_won(soup)
                }
                logger.info("transformed match data")
                match_data.append(match_info)
            except Exception as e:
                logger.error(
                    "Error processing match data: {}".format(e), exc_info=True)
            logger.debug("Match data: {}".format(match_data))
            return match_data

    def process_draw_data(self, round, soup):
        if soup:
            match_containers = soup.find_all(
                'div', class_=RoundDefaults.MATCH_CONTAINER_CLASS.value)
            match_data = []

            for match in match_containers:
                logger.info("Processing match data")
                try:
                    home_team = match.find(
                        RoundDefaults.MATCH_CLASS_TAG.value, class_=RoundDefaults.HOME_TEAM_CLASS.value).text.strip()
                    logger.info("Home team: {}".format(home_team))
                    away_team = match.find(
                        RoundDefaults.MATCH_CLASS_TAG.value, class_=RoundDefaults.AWAY_TEAM_CLASS.value).text.strip()
                    logger.info("Away team: {}".format(away_team))
                    match_url = match.find(
                        RoundDefaults.MATCH_URL_TAG.value,   class_=RoundDefaults.MATCH_URL_CLASS.value)[RoundDefaults.MATCH_HREF.value]
                    stadium = match.find(
                        RoundDefaults.MATCH_CLASS_TAG.value, class_=RoundDefaults.STADIUM_CLASS.value).text.strip().strip("\n            ")

                    match_info = {
                        'HomeTeam': home_team,
                        'AwayTeam': away_team,
                        'url': match_url,
                        'Stadium': stadium
                    }

                    match_data.append(match_info)
                    logger.debug("Match Info: {}".format(match_info))
                except Exception as e:
                    logger.error(f"Error processing match data: {e}")

            return match_data
        else:
            logger.error("Soup object is empty")
            return None

    def process_teams_data(self, soup, team_name):
        '''
        Process the data
        :param soup: The data to process
        :param team_name: The team name to process
        :return: The processed data
        '''
        if soup:
            logger.info("Processing {} data...".format(self.stat))
            table_element = soup.find(
                TeamDefaults.TEAMS_CONTAINER_TAG.value, class_=TeamDefaults.TEAMS_CONTAINER_CLASS.value)
            logger.debug("Table element: {}".format(table_element))
            if table_element:
                for row in table_element.select(TeamDefaults.TEAMS_ELEMENT_SELECT.value):
                    logger.debug("Table element row: {}".format(row))
                    team_name_element = row.find(
                        TeamDefaults.TEAMS_ROW_TAG.value, class_=TeamDefaults.TEAMS_ROW_CLASS.value)
                    logger.debug(
                        "Team name element: {}".format(team_name_element))
                    if team_name_element and team_name_element.get_text(strip=True).replace(" ", "") == team_name:
                        return process_table_row(row, self.stat)
        return None
