from util.scraper import WebScraper
from util.data_processing import process_table_row
from util.defaults import Url
from util.logger import get_logger
from teams.defaults import TeamDefaults

logger = get_logger()
logger.setLevel("DEBUG")


class Stats:

    def __init__(self, url, stat):
        logger.info("Initialising Goals")
        logger.debug("URL: {}".format(url))
        self.url = url
        self.stat = stat
        self.scraper = WebScraper(self.url)

    def get_all_data(self):
        logger.info("Getting all data")
        return self.scraper.load_page(TeamDefaults.TEAMS_PATH.value)

    def process_data(self, soup, team_name):
        logger.info("Processing data")
        if soup:
            table_element = soup.find(
                TeamDefaults.TEAMS_FIND_TAG.value, class_=TeamDefaults.TEAMS_FIND.value)
            logger.debug("Table element: {}".format(table_element))
            if table_element:
                for row in table_element.select(TeamDefaults.TEAMS_ELEMENT_SELECT.value):
                    logger.debug("Table element row: {}".format(row))
                    team_name_element = row.find(
                        TeamDefaults.TEAMS_ROW_FIND_TAG.value, class_=TeamDefaults.TEAMS_ROW_FIND.value)
                    logger.debug(
                        "Team name element: {}".format(team_name_element))
                    if team_name_element and team_name_element.get_text(strip=True).replace(" ", "") == team_name:
                        return process_table_row(row, self.stat)
        return None
