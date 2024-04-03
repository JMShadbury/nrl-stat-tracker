"""Module to retrieve and process data."""

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.logger import configure_logger
import json
from util.json_client import JSONClient


# Configure logger
logger = configure_logger("get_data.log")

def transform_data_for_display(items):
    """Transform data for display."""
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
        logger.info("Data saved to %s", filepath)
    except IOError as e:
        logger.error(f"Failed to save data: {e}")

def process_team_data(team_names):
    """Process and save team data."""
    for team_name in team_names:
        client = JSONClient(team_name)
        raw_data = client.read_data()
        if raw_data:
            save_json(raw_data, 'app/teams', f'{team_name}.json')

def main():
    """Main function."""
    with open(os.path.join(os.path.dirname(__file__), "teams"), "r") as f:
        team_names = list(f.read().splitlines())
    process_team_data(team_names)
    
    client = JSONClient("Ladder")
    ladder_data = client.read_data()
    if ladder_data:
        save_json(ladder_data, 'app/ladder', 'ladder_data.json')

if __name__ == '__main__':
    main()
