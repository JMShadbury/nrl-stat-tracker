from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Firefox()

    def load_page(self, xpath, delay=10):
        self.driver.get(self.url)
        try:
            WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
            return BeautifulSoup(self.driver.page_source, 'html.parser')
        except TimeoutException:
            print("Couldn't load page")
            return None

    def close(self):
        self.driver.quit()
