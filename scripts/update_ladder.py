import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import boto3

# Initialize DynamoDB client and table
dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-2')
table = dynamodb.Table('Ladder')

url = "https://www.nrl.com/ladder/"

# Configure Selenium WebDriver
driver = webdriver.Firefox()
driver.get(url)

# Wait for the desired element to be present
delay = 1
try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//tr[@q-component="ladder-body-row"]')))

    # Continue with the rest of the script
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table_element = soup.find('table', {"id": "ladder-table"})

    if table_element:
        for row in table_element.select('tr[q-component="ladder-body-row"]'):
            pos_text = row.select_one('.ladder-position')
            if pos_text:
                pos_text = pos_text.get_text(strip=True)

            team_text = row.select_one('.ladder-club').get_text(strip=True)
            played_text = row.select_one('.ladder__item:nth-of-type(5)').get_text(strip=True)
            points_text = row.select_one('.ladder__item:nth-of-type(6)').get_text(strip=True)
            wins_text   = row.select_one('.ladder__item:nth-of-type(7)').get_text(strip=True)
            drawn_text  = row.select_one('.ladder__item:nth-of-type(8)').get_text(strip=True)
            lost_text   = row.select_one('.ladder__item:nth-of-type(9)').get_text(strip=True)
            byes_text   = row.select_one('.ladder__item:nth-of-type(10)').get_text(strip=True)
            for_text    = row.select_one('.ladder__item:nth-of-type(11)').get_text(strip=True)
            against_text= row.select_one('.ladder__item:nth-of-type(12)').get_text(strip=True)
            diff_text   = row.select_one('.ladder__item:nth-of-type(13)').get_text(strip=True)
            home_text   = row.select_one('.ladder__item:nth-of-type(14)').get_text(strip=True)
            away_text   = row.select_one('.ladder__item:nth-of-type(15)').get_text(strip=True)
            form_text   = row.select_one('.ladder__item:nth-of-type(16)').get_text(strip=True)


            if pos_text and team_text and played_text and points_text:
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

                print(data)
                table.put_item(Item=data)

        print("Data inserted into DynamoDB.")
    else:
        print("Table not found in the HTML.")

except TimeoutException:
    print("Couldn't load page")

finally:
    # Close the WebDriver
    driver.quit()
