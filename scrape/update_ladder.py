"""Module to update ladder data."""

# pylint: disable=E0401
# pylint: disable=C0413
# pylint: disable=W0718
# pylint: disable=C0411

from util.scraper import WebScraper
from util.json_client import JSONClient
from util.defaults import Url
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.logger import configure_logger

# Configure logger
logger = configure_logger("UpdateLadder.log")


class UpdateLadder:
    """Class to update ladder data."""

    def __init__(self):
        """Initialize UpdateLadder."""
        logger.info("Initializing UpdateLadder")
        self.scraper = WebScraper(Url.LADDER.value)
        self.db_client = JSONClient("Ladder")
        logger.info("UpdateLadder Initialized")

    def get_text(self, row, selector):
        """Get text from HTML element."""
        element = row.select_one(selector)
        return element.get_text(strip=True) if element else None

    def update_ladder(self):
        """Update ladder data."""
        logger.info("Updating ladder data")
        try:
            soup = self.scraper.load_page(
                '//tr[@q-component="ladder-body-row"]')
            if soup:
                table_element = soup.find('table', {"id": "ladder-table"})
                if table_element:
                    for row in table_element.select('tr[q-component="ladder-body-row"]'):
                        data = {
                            'Pos': int(self.get_text(row, '.ladder-position')),
                            'TeamName': self.get_text(row, '.ladder-club'),
                            'Played': int(self.get_text(row, '.ladder__item:nth-of-type(5)')),
                            'Points': int(self.get_text(row, '.ladder__item:nth-of-type(6)')),
                            'Wins': int(self.get_text(row, '.ladder__item:nth-of-type(7)')),
                            'Drawn': int(self.get_text(row, '.ladder__item:nth-of-type(8)')),
                            'Lost': int(self.get_text(row, '.ladder__item:nth-of-type(9)')),
                            'Byes': int(self.get_text(row, '.ladder__item:nth-of-type(10)')),
                            'For': int(self.get_text(row, '.ladder__item:nth-of-type(11)')),
                            'Against': int(self.get_text(row, '.ladder__item:nth-of-type(12)')),
                            'Diff': int(self.get_text(row, '.ladder__item:nth-of-type(13)')),
                            'Home': self.get_text(row, '.ladder__item:nth-of-type(14)'),
                            'Away': self.get_text(row, '.ladder__item:nth-of-type(15)'),
                            'Form': self.get_text(row, '.ladder__item:nth-of-type(16)')
                        }
                        self.db_client.insert_item(data)
        except Exception as e:
            logger.error("Error updating ladder: %s", e, exc_info=True)
        finally:
            self.scraper.close()
            logger.info("Ladder update process completed")


if __name__ == '__main__':
    update_ladder = UpdateLadder()
    update_ladder.update_ladder()
