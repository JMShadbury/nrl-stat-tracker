""" This module contains functionality for scraping statistics from the NRL website. """

from util.scraper import WebScraper
from stats.constants import TeamDefaults
import sys
import os
sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../..')))
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
        logger.info(f"Initialising {stat}")
        logger.debug(f"URL: {url}")
        self.url = url
        self.stat = stat
        self.scraper = WebScraper(self.url)

    def get_data(self):
        '''
        Get all the data from the URL
        :return: The data from the URL
        '''

        logger.info(f"Scrape data for stat: {self.stat}...")
        return self.scraper.load_page(TeamDefaults.TEAMS_PATH.value, TeamDefaults.TEAMS_AVERAGE_BUTTON.value)

    def process_teams_data(self, soup, team_name):
        '''
        Process the data
        :param soup: The data to process
        :param team_name: The team name to process
        :return: The processed data
        '''
        if soup:
            logger.info(f"Processing {self.stat} data...")
            table_element = soup.find(
                TeamDefaults.TEAMS_CONTAINER_TAG.value, class_=TeamDefaults.TEAMS_CONTAINER_CLASS.value)
            logger.debug(f"Table element: {table_element}")
            if table_element:
                for row in table_element.select(TeamDefaults.TEAMS_ELEMENT_SELECT.value):
                    logger.debug(f"Table element row: {row}")
                    team_name_element = row.find(
                        TeamDefaults.TEAMS_ROW_TAG.value, class_=TeamDefaults.TEAMS_ROW_CLASS.value)
                    logger.debug(f"Team name element: {team_name_element}")
                    if team_name_element and team_name_element.get_text(strip=True).replace(" ", "") == team_name:
                        return process_table_row(row, self.stat)
        return None
