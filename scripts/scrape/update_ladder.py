from util.scraper import WebScraper
from util.dynamodb import DynamoDBClient
from util.defaults import Url
from util.logger import configure_logger

logger = configure_logger("UpdateLadder.log")
logger.setLevel("INFO")  # Adjusted for typical production use

class UpdateLadder:
    def __init__(self):
        logger.info("Initializing UpdateLadder")
        self.scraper = WebScraper(Url.LADDER.value)
        self.db_client = DynamoDBClient("Ladder")
        logger.info("UpdateLadder Initialized")

    def get_text(self, row, selector):
        element = row.select_one(selector)
        return element.get_text(strip=True) if element else None

    def update_ladder(self):
        logger.info("Updating ladder data")
        try:
            soup = self.scraper.load_page('//tr[@q-component="ladder-body-row"]')
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
            logger.error(f"Error updating ladder: {e}", exc_info=True)
        finally:
            self.scraper.close()
            logger.info("Ladder update process completed")

update_ladder = UpdateLadder()
update_ladder.update_ladder()