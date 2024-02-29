import pandas as pd
import os
import glob
from util.logger import get_logger
import json

logger = get_logger()

def load_rounds_data():
    with open('rounds/rounds_data.json', 'r') as file:
        rounds_data = json.load(file)
    return rounds_data

def load_data():
    '''
    Load data from JSON files and create a DataFrame
    
    Returns:
        pd.DataFrame: DataFrame containing the data
    '''
    logger.info("Loading data")
    data_dir = 'teams'
    json_files = glob.glob(os.path.join(data_dir, '*.json'))
    logger.debug(f"JSON files: {json_files}")

    data_frames = [pd.read_json(file) for file in json_files]
    logger.debug(f"Data frames: {data_frames}")
    all_teams_data = pd.concat(data_frames)
    logger.debug(f"All teams data: {all_teams_data}")
    all_teams_data['TeamName'] = all_teams_data['TeamName'].astype(str)
    logger.debug(f"All teams data: {all_teams_data}")

    logger.info("Data loaded")

    logger.info("Creating DataFrame")

    df = pd.DataFrame(all_teams_data)
    df.set_index('TeamName', inplace=True)
    logger.debug("DataFrame created -: {}".format(df))
    logger.info("DataFrame Created")

    return df

team_data = load_data()
