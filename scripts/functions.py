import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import boto3

def get_points(team_name):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')


    url = "https://www.nrl.com/stats/teams/?competition=111&season=2023&stat=76"
    driver = webdriver.Firefox()
    driver.get(url)
    delay = 10

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//tbody[@class="table-tbody u-white-space-no-wrap"]')))
    except TimeoutException:
        print("Couldn't load page")
        driver.quit()
        return None  # Return None to indicate an issue

    # get the table element
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_element = soup.find('tbody', class_='table-tbody u-white-space-no-wrap')

    table = dynamodb.Table(team_name)

    if table_element:
        for row in table_element.select('tr.table-tbody__tr'):
            columns = row.find_all(['td', 'th'])

            # Check if the row is valid
            if len(columns) == 5:
                team_name_element = columns[2].find('span', class_='u-font-weight-600')
                points_element = columns[4]

                # Check if team_name_element exists and is not None
                if team_name_element and team_name_element.text.strip():
                    team_name = team_name_element.text.strip().replace(" ", "")  # Remove spaces
                    points = points_element.text.strip()

                    if team_name_element.lower() == team_name.replace(" ", "").lower():  # Remove spaces
                        data = {
                            'TeamName': team_name_element.text.strip(),
                            'Points': int(points),
                        }

                        return data

                    else:
                        print("Team name does not match. Skipping.")
                else:
                    print("Team name element is missing or empty. Skipping.")
            else:
                print("Invalid data structure. Skipping.")

        return None
    else:
        print("Table not found in the HTML.")
    driver.quit()


def get_trys(team_name):
    dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

    url = "https://www.nrl.com/stats/teams/?competition=111&season=2023&stat=38"
    driver = webdriver.Firefox()
    driver.get(url)
    delay = 10

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//tbody[@class="table-tbody u-white-space-no-wrap"]')))
    except TimeoutException:
        print("Couldn't load page")

    # get the table element
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_element = soup.find('tbody', class_='table-tbody u-white-space-no-wrap')
    count = 5

    if table_element:
        for row in table_element.select('tr.table-tbody__tr'):
            columns = row.find_all(['td', 'th'])
            
            # Check if the row is valid
            if len(columns) == 5:
                team_name_element = columns[2].find('span', class_='u-font-weight-600')
                played_element = columns[3]
                tries_element = columns[4]

                if team_name_element and played_element and tries_element:
                    team_name = team_name_element.text.strip()
                    played = played_element.text.strip()
                    tries = tries_element.text.strip()

                    if team_name.replace(" ", "").lower() == team_name.replace(" ", "").lower():
                        data = {
                            'TeamName': team_name,
                            'Played': int(played),
                            'Tries': int(tries),
                        }
                        
                        print(data)
                        return data
                    else:
                        print("Team name does not match. Skipping.")
                else:
                    print("Some data is missing in this row. Skipping.")
            else:
                print("Invalid data structure. Skipping.")
            driver.quit()

