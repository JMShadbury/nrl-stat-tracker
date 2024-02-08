from util.scraper import WebScraper
from util.data_processing import process_table_row
from util.logger import get_logger
from stats.constants import TeamDefaults, RoundDefaults, GameDefaults

logger = get_logger()
logger.setLevel("DEBUG")


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
        logger.info("Getting all data")
        return self.scraper.load_page(GameDefaults.GAME_PATH.value)

    def get_all_draw_data(self):
        '''
        Get all the data from the URL
        :return: The data from the URL
        '''
        logger.info("Getting all data")
        return self.scraper.load_page(RoundDefaults.MATCH_PATH.value)

    def get_all_teams_data(self):
        '''
        Get all the data from the URL
        :return: The data from the URL
        '''
        logger.info("Getting all data")
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

                    game_previous_info = {
                        'PreviousHomeScore': home_score,
                        'PreviousAwayScore': away_score,
                        'PreviousHomeTeam': get_home_name(game),
                        'PreviousAwayTeam': get_away_name(game)
                    }

                    game_previous_data.append(game_previous_info)

                except Exception as e:
                    logger.error(
                        "Error processing game data: {}".format(e), exc_info=True)
            for game in game_previous_data:
                try:
                    match_info = {
                        'PreviousHomeTeams': game['PreviousHomeTeam'],
                        'PreviousAwayTeams': game['PreviousAwayTeam'],
                        'PreviousHomeScores': game['PreviousHomeScore'],
                        'PreviousAwayScores': game['PreviousAwayScore'],
                        'GamesPlayed': get_games_played(soup),
                        'AwayGamesWon': get_away_games_won(soup),
                        'HomeGamesWon': get_home_games_won(soup)
                    }

                    match_data.append(match_info)
                except Exception as e:
                    logger.error(
                        "Error processing match data: {}".format(e), exc_info=True)
            logger.info("Match data: {}".format(match_data))
            return match_data

    def process_draw_data(self, round, soup):
        if soup:
            match_containers = soup.find_all(
                'div', class_=RoundDefaults.MATCH_CONTAINER_CLASS.value)
            match_data = []

            for match in match_containers:
                try:
                    home_team = match.find(
                        RoundDefaults.MATCH_CLASS_TAG.value, class_=RoundDefaults.HOME_TEAM_CLASS.value).text.strip()
                    away_team = match.find(
                        RoundDefaults.MATCH_CLASS_TAG.value, class_=RoundDefaults.AWAY_TEAM_CLASS.value).text.strip()
                    match_url = match.find(
                        RoundDefaults.MATCH_URL_TAG.value,   class_=RoundDefaults.MATCH_URL_CLASS.value)[RoundDefaults.MATCH_HREF.value]
                    stadium = match.find(
                        RoundDefaults.MATCH_CLASS_TAG.value, class_=RoundDefaults.STADIUM_CLASS.value).text.strip()

                    match_info = {
                        'HomeTeam': home_team,
                        'AwayTeam': away_team,
                        'url': match_url,
                        'Stadium': stadium
                    }

                    match_data.append(match_info)
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
