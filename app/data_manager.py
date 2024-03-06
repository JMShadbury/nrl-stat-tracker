"""
This module handles loading and aggregating team data from JSON files into a pandas DataFrame.
"""

# pylint: disable=E0401

import os
import glob
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.logger import get_logger
import pandas as pd


logger = get_logger()


def load_rounds_data():
    """
    Load data from a JSON file into a dictionary.

    Returns:
        dict: Data loaded from the rounds_data.json file.
    """
    with open('rounds/rounds_data.json', 'r', encoding='utf-8') as file:
        rounds_data = json.load(file)
    return rounds_data


def load_data():
    """
    Load data from JSON files in the 'teams' directory and create a DataFrame.

    Returns:
        pd.DataFrame: DataFrame containing the aggregated data from all team files.
    """
    logger.info("Loading data")
    data_dir = 'teams'
    json_files = glob.glob(os.path.join(data_dir, '*.json'))
    logger.debug("JSON files found: %s", json_files)

    data_frames = [pd.read_json(file) for file in json_files]
    all_teams_data = pd.concat(data_frames)
    all_teams_data['TeamName'] = all_teams_data['TeamName'].astype(str)

    logger.info("Data loaded and DataFrame creation started")
    df = pd.DataFrame(all_teams_data)
    df.set_index('TeamName', inplace=True)

    logger.info("DataFrame created")
    return df


team_data = load_data()
