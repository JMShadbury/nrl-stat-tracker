from util.logger import get_logger

logger = get_logger()

logger.setLevel("DEBUG")


def format_team_name_for_dynamodb(team_name):
    logger.debug("Formatting team name -  {} -  for DynamoDB".format(team_name))
    return ''.join(word.capitalize() for word in team_name.split())

def process_table_row_points(row):
    logger.debug("Processing table row points: {}".format(row))
    played = row.select_one('td:nth-of-type(4)').get_text(strip=True)
    points = row.select_one('td:nth-of-type(5)').get_text(strip=True)
    
    data = {
        'TeamName': row.select_one('span.u-font-weight-600').get_text(strip=True),
        'Played': played,
        'Points': points 
    }
    
    logger.debug("Processed data: {}".format(data))

    return data
    
def process_table_row_tries(row):
    logger.debug("Processing table row tries: {}".format(row))
    played = row.select_one('td:nth-of-type(4)').get_text(strip=True)
    tries = row.select_one('td:nth-of-type(5)').get_text(strip=True)
    
    data = {
        'TeamName': row.select_one('span.u-font-weight-600').get_text(strip=True),
        'Played': played,
        'Tries': tries 
    }
    
def process_table_row_goals(row):
    logger.debug("Processing table row goals: {}".format(row))
    played = row.select_one('td:nth-of-type(4)').get_text(strip=True)
    goals = row.select_one('td:nth-of-type(5)').get_text(strip=True)
    
    data = {
        'TeamName': row.select_one('span.u-font-weight-600').get_text(strip=True),
        'Played': played,
        'Goals': goals 
    }
    
    logger.debug("Processed data: {}".format(data))
    return data
