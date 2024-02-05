import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from util.logger import configure_logger
import json

# Configure logger
logger = configure_logger("DynamoDBToGrafana")

def get_dynamodb_client():
    try:
        # Initialize a DynamoDB client
        dynamodb_client = boto3.client('dynamodb')
        return dynamodb_client
    except NoCredentialsError:
        print("Credentials not available")
        return None

def fetch_ladder_data_from_dynamodb(client, table_name):
    """Fetch ladder data from a DynamoDB table."""
    try:
        logger.info(f"Retrieving data from DynamoDB table: {table_name}")
        response = client.scan(TableName=table_name)
        logger.info("Data retrieved successfully.")
        return response['Items']
    except ClientError as e:
        logger.error(f"An error occurred while fetching data from DynamoDB: {e}")
        return None

def prepare_ladder_data_for_display(items):
    """Prepare ladder data for display from DynamoDB items."""
    return [
        {key: int(value['N']) if 'N' in value else value['S']
         for key, value in item.items()} for item in items
    ]

def save_json_data(data, directory, filename):
    """Save data to a JSON file in the specified directory."""
    if not data:
        logger.error("No data to write to JSON.")
        return

    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        logger.info(f"Data saved to {filepath}")
    except IOError as e:
        logger.error(f"Failed to write data to JSON: {e}")


def main():
    # Initialize DynamoDB client
    dynamodb_client = get_dynamodb_client()
    if not dynamodb_client:
        return
    
    # Process team data
    with open("data/teams", "r") as f:
        team_names = f.read().splitlines()
    team_names = {team.split(":")[0]: team.split(":")[1] for team in team_names}
    
    for team_name in team_names:
        print(team_name)
        raw_data = fetch_ladder_data_from_dynamodb(dynamodb_client, team_name)
        if raw_data:
            transformed_data = prepare_ladder_data_for_display(raw_data)
            save_json_data(transformed_data, 'data', f'{team_name}.json')
    
    # Process ladder data
    ladder_raw_data = fetch_ladder_data_from_dynamodb(dynamodb_client, "Ladder")
    if ladder_raw_data:
        ladder_transformed_data = prepare_ladder_data_for_display(ladder_raw_data)
        save_json_data(ladder_transformed_data, 'ladder', 'ladder_data.json')


if __name__ == '__main__':
    main()
