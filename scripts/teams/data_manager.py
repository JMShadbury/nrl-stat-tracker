import pandas as pd
import os
import glob
from util.logger import get_logger

logger = get_logger()

def load_data():
    logger.info("Loading data")
    data_dir = 'scripts/data'
    json_files = glob.glob(os.path.join(data_dir, '*.json'))
    logger.info(f"JSON files: {json_files}")

    data_frames = [pd.read_json(file) for file in json_files]
    logger.info(f"Data frames: {data_frames}")
    all_teams_data = pd.concat(data_frames)
    logger.info(f"All teams data: {all_teams_data}")
    all_teams_data['TeamName'] = all_teams_data['TeamName'].astype(str)
    logger.info(f"All teams data: {all_teams_data}")
    
    logger.info("Data loaded")
    
    logger.info("Creating DataFrame")

    df = pd.DataFrame(all_teams_data)
    df.set_index('TeamName', inplace=True)
    
    logger.info("DataFrame created -: {}".format(df))

    return df


# Load the data once and keep it in memory
team_data = load_data()