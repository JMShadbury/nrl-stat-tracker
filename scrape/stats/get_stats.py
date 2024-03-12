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
from stats.constants import TeamDefaults
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

    def get_all_teams_data(self):
        '''
        Get all the data from the URL
        :return: The data from the URL
        '''
        return self.scraper.load_page(TeamDefaults.TEAMS_PATH.value)

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

