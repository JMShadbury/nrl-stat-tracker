def process_table_row(row):
    columns = row.find_all(['td', 'th'])
    if len(columns) == 5:
        team_name_element = columns[2].find('span', class_='u-font-weight-600')
        value_element = columns[4]

        if team_name_element and value_element:
            team_name = team_name_element.text.strip().replace(" ", "")  # Remove spaces
            value = value_element.text.strip()

            return {
                'TeamName': team_name,
                'Value': int(value)
            }
    return None

def format_team_name_for_dynamodb(team_name):
    return ''.join(word.capitalize() for word in team_name.split())
