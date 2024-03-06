"""Module for web scraping."""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
# pylint: disable=E0401
from common.logger import get_logger

logger = get_logger()


class WebScraper:
    """Class to perform web scraping."""

    source = None
    
    def __init__(self, url):
        '''
        Initialise the WebScraper
        :param url: The URL to scrape
        '''
        logger.debug("Initialising WebScraper")
        self.url = url
        logger.debug("Setting URL: %s", self.url)
        options = Options()
        options.headless = True
        options.add_argument("-headless") 
        self.driver = webdriver.Firefox(options=options)

    def load_page(self, xpath, delay=0):
        '''
        Load the page and return the source
        :param xpath: The xpath to find
        :param delay: The delay to wait for
        :return: The source of the page
        '''
        if not self.source:
            logger.debug("Loading page with xpath: %s", xpath)
            self.driver.get(self.url)
            logger.info("Getting all data from webpage: %s", self.url)
            try:
                WebDriverWait(self.driver, delay).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
                source = BeautifulSoup(self.driver.page_source, 'html.parser')
                self.source = source
                self.close()
                return source
            except TimeoutException:
                logger.error("Couldn't load page")
                self.close()
                return None
            except Exception as e:
                logger.error("An error occurred: %s", e)
                self.close()
                return None

    def close(self):
        '''
        Close the driver
        '''
        logger.debug("Closing Firefox driver")
        self.driver.quit()
