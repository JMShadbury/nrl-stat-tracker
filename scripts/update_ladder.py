from util.scraper import WebScraper
from util.dynamodb import DynamoDBClient
from util.defaults import Url
from util.logger import configure_logger

logger = configure_logger("UpdateLadder")
logger.setLevel("DEBUG")


class UpdateLadder:
    def __init__(self):
        '''
        Initialise the UpdateLadder class
        '''
        logger.info("Initialising UpdateLadder")
        self.scraper = WebScraper(Url.LADDER.value)
        logger.debug(f"Setting URL: {Url.LADDER.value}")
        self.db_client = DynamoDBClient("Ladder")
        logger.debug("Setting DynamoDB client {self.db_client}")
        logger.info("Initialised UpdateLadder")

    def update_ladder(self):
        '''
        Update the ladder
        '''
        try:
            soup = self.scraper.load_page(
                '//tr[@q-component="ladder-body-row"]')
            if soup:
                table_element = soup.find('table', {"id": "ladder-table"})
                if table_element:
                    for row in table_element.select('tr[q-component="ladder-body-row"]'):
                        pos_text = row.select_one('.ladder-position')
                        if pos_text:
                            pos_text = pos_text.get_text(strip=True)
                            team_text = row.select_one(
                                '.ladder-club').get_text(strip=True)
                            played_text = row.select_one(
                                '.ladder__item:nth-of-type(5)').get_text(strip=True)
                            points_text = row.select_one(
                                '.ladder__item:nth-of-type(6)').get_text(strip=True)
                            wins_text = row.select_one(
                                '.ladder__item:nth-of-type(7)').get_text(strip=True)
                            drawn_text = row.select_one(
                                '.ladder__item:nth-of-type(8)').get_text(strip=True)
                            lost_text = row.select_one(
                                '.ladder__item:nth-of-type(9)').get_text(strip=True)
                            byes_text = row.select_one(
                                '.ladder__item:nth-of-type(10)').get_text(strip=True)
                            for_text = row.select_one(
                                '.ladder__item:nth-of-type(11)').get_text(strip=True)
                            against_text = row.select_one(
                                '.ladder__item:nth-of-type(12)').get_text(strip=True)
                            diff_text = row.select_one(
                                '.ladder__item:nth-of-type(13)').get_text(strip=True)
                            home_text = row.select_one(
                                '.ladder__item:nth-of-type(14)').get_text(strip=True)
                            away_text = row.select_one(
                                '.ladder__item:nth-of-type(15)').get_text(strip=True)
                            form_text = row.select_one(
                                '.ladder__item:nth-of-type(16)').get_text(strip=True)

                            data = {
                                'Pos': int(pos_text),
                                'TeamName': team_text,
                                'Played': int(played_text),
                                'Points': int(points_text),
                                'Wins': int(wins_text),
                                'Drawn': int(drawn_text),
                                'Lost': int(lost_text),
                                'Byes': int(byes_text),
                                'For': int(for_text),
                                'Against': int(against_text),
                                'Diff': int(diff_text),
                                'Home': home_text,
                                'Away': away_text,
                                'Form': form_text
                            }

                            self.db_client.insert_item(data)
                    self.scraper.close()
        except Exception as e:
            logger.error(f"Error updating ladder: {e}", exc_info=True)
            self.scraper.close()
            raise e


update_ladder = UpdateLadder()
update_ladder.update_ladder()
