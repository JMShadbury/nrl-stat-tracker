from util.scraper import WebScraper
from util.data_processing import process_table_row
from util.defaults import Url
from teams.defaults import TeamDefaults

class Tries:
    def __init__(self):
        self.url = Url.TEAM_TRIES.value
        self.scraper = WebScraper(self.url)

    def get_all_tries_data(self):
        return self.scraper.load_page(TeamDefaults.TRIES_TABLE_ELEMENT.value)

    def process_tries_data(self, soup, team_name):
        if soup:
            table_element = soup.find(TeamDefaults.TRIES_ELEMENT_TYPE.value, class_=TeamDefaults.TRIES_TABLE_ELEMENT.value)
            print(table_element)
            if table_element:
                for row in table_element.select(TeamDefaults.TRIES_ELEMENT.value):
                    team_name_element = row.find('span', class_='u-font-weight-600')
                    if team_name_element and team_name_element.get_text(strip=True) == team_name:
                        return process_table_row(row)
        return None

