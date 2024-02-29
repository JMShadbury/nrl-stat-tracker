import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from util.json_client import JSONClient
from util.logger import configure_logger
import json

# Configure logger
logger = configure_logger("get_data.log")

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

def process_team_data(team_names):
    """Process and save team data."""
    for team_name in team_names:
        client = JSONClient(team_name)
        raw_data = client.read_data()
        if raw_data:
            save_json(raw_data, 'scripts/app/data', f'{team_name}.json')

def main():
    with open("scripts/app/data/teams", "r") as f:
        team_names = [team.split(":")[0] for team in f.read().splitlines()]
    process_team_data(team_names)
    
    
    client = JSONClient("Ladder")
    ladder_data = client.read_data()
    if ladder_data:
        save_json(ladder_data, 'scripts/app/ladder', 'ladder_data.json')
        
    client = JSONClient("NRL2024Rounds")
    rounds_data = client.read_data()
    if rounds_data:
        save_json(rounds_data, 'scripts/app/rounds', 'rounds_data.json')

if __name__ == '__main__':
    main()
