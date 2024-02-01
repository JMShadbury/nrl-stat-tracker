from util.scraper import WebScraper
from util.data_processing import process_table_row
from util.defaults import Url

class Tries:
    def __init__(self):
        self.url = Url.TRIES.value
        self.scraper = WebScraper(self.url)

    def get_tries_data(self):
        soup = self.scraper.load_page('//tbody[@class="table-tbody u-white-space-no-wrap"]')
        if soup:
            table_element = soup.find('tbody', class_='table-tbody u-white-space-no-wrap')
            if table_element:
                return [process_table_row(row) for row in table_element.select('tr.table-tbody__tr')]
        return None
