from util.scraper import WebScraper
from util.data_processing import process_table_row
from util.defaults import Url
from teams.defaults import TeamDefaults

class Points:
    def __init__(self):
        self.url = Url.TEAM_POINTS.value
        self.scraper = WebScraper(self.url)

    def get_all_points_data(self):
        return self.scraper.load_page(TeamDefaults.POINTS_TABLE_ELEMENT.value)

    def process_points_data(self, soup, team_name):
        if soup:
            table_element = soup.find(TeamDefaults.POINTS_ELEMENT_TYPE.value, class_=TeamDefaults.POINTS_TABLE_ELEMENT.value)
            if table_element:
                for row in table_element.select(TeamDefaults.POINTS_ELEMENT.value):
                    team_name_element = row.find('span', class_='u-font-weight-600')
                    if team_name_element and team_name_element.get_text(strip=True) == team_name:
                        return process_table_row(row)
        return None

