from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from util.logger import get_logger

logger = get_logger()


class WebScraper:
    def __init__(self, url):
        '''
        Initialise the WebScraper
        :param url: The URL to scrape
        '''
        logger.info("Initialising WebScraper")
        self.url = url
        logger.info(f"Setting URL: {self.url}")
        self.driver = webdriver.Firefox()

    def load_page(self, xpath, delay=10):
        '''
        Load the page and return the source
        :param xpath: The xpath to find
        :param delay: The delay to wait for
        :return: The source of the page
        '''
        logger.info(f"Loading page with xpath: {xpath}")
        self.driver.get(self.url)
        logger.debug(f"URL: {self.url}")
        try:
            WebDriverWait(self.driver, delay).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
            source = BeautifulSoup(self.driver.page_source, 'html.parser')
            logger.info("Page data found, closing driver")
            self.close()
            return source
        except TimeoutException:
            print("Couldn't load page")
            self.close()
            return None

    def close(self):
        '''
        Close the driver
        '''
        logger.debug("Closing Firefox driver")
        self.driver.quit()
