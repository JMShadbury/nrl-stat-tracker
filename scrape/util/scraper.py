from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from util.logger import get_logger

logger = get_logger()


class WebScraper:
    
    source = None
    
    def __init__(self, url):
        '''
        Initialise the WebScraper
        :param url: The URL to scrape
        '''
        logger.debug("Initialising WebScraper")
        self.url = url
        logger.debug(f"Setting URL: {self.url}")
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
            logger.debug(f"Loading page with xpath: {xpath}")
            self.driver.get(self.url)
            logger.info(f"Getting all data from webpage: {self.url}")
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
                logger.error(f"An error occurred: {e}")
                self.close()
                return None

    def close(self):
        '''
        Close the driver
        '''
        logger.debug("Closing Firefox driver")
        self.driver.quit()
