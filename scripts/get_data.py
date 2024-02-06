import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from util.logger import configure_logger
import json

# Configure logger
logger = configure_logger("GetDataFromDynamoDB.log")

def get_dynamodb_client():
    try:
        return boto3.client('dynamodb')
    except NoCredentialsError as e:
        logger.error(f"Credentials not available: {e}")
        return None

def fetch_data_from_dynamodb(client, table_name):
    """Fetch data from a DynamoDB table."""
    try:
        logger.info(f"Retrieving data from DynamoDB table: {table_name}")
        return client.scan(TableName=table_name)['Items']
    except ClientError as e:
        logger.error(f"Error fetching data from DynamoDB: {e}")
        return None

def transform_data_for_display(items):
    """Transform DynamoDB items for display."""
    return [{key: int(value['N']) if 'N' in value else value['S']
             for key, value in item.items()} for item in items]

def save_json(data, directory, filename):
    """Save data to JSON in specified directory."""
    if not data:
        logger.error("No data to save.")
        return

    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        logger.info(f"Data saved to {filepath}")
    except IOError as e:
        logger.error(f"Failed to save data: {e}")

def process_team_data(client, team_names):
    """Process and save team data."""
    for team_name in team_names:
        raw_data = fetch_data_from_dynamodb(client, team_name)
        if raw_data:
            transformed_data = transform_data_for_display(raw_data)
            save_json(transformed_data, 'scripts/data', f'{team_name}.json')

def main():
    dynamodb_client = get_dynamodb_client()
    if not dynamodb_client:
        return

    with open("scripts/data/teams", "r") as f:
        team_names = [team.split(":")[0] for team in f.read().splitlines()]
    
    process_team_data(dynamodb_client, team_names)

    ladder_data = fetch_data_from_dynamodb(dynamodb_client, "Ladder")
    if ladder_data:
        transformed_ladder_data = transform_data_for_display(ladder_data)
        save_json(transformed_ladder_data, 'ladder', 'ladder_data.json')

if __name__ == '__main__':
    main()
