import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import boto3

dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')

f = open("data/teams", "r")
teams = f.read().splitlines()
f.close()

teams = {team.split(":")[0]: team.split(":")[1] for team in teams}

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

for current_team, team_id in teams.items():
    table = dynamodb.Table(current_team)
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

                    if team_name.replace(" ", "").lower() == current_team.replace(" ", "").lower():
                        data = {
                            'TeamName': team_name,
                            'Played': int(played),
                            'Tries': int(tries),
                        }

                        print(data)

                        table.put_item(Item=data)
                    else:
                        print("Team name does not match. Skipping.")
                else:
                    print("Some data is missing in this row. Skipping.")
            else:
                print("Invalid data structure. Skipping.")
driver.quit()
