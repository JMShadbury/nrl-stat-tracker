"""Module for interacting with JSON files."""


import json
import os
import sys
from util.exceptions import InvalidJSON, InvalidData
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '../..')))
from common.logger import get_logger


logger = get_logger()

path = "scrape/all_data/"


class JSONClient:
    """Class for interacting with JSON files."""

    def __init__(self, file_name):
        '''
        Initialise the JSON client

        :param file_name: The name of the JSON file
        '''
        self.file_name = file_name
        logger.debug(
            f"Initialising JSON client with file name: {path + self.file_name}")
        # Create the file if it does not exist
        if not os.path.exists(path + self.file_name):
            with open(path + self.file_name, 'w') as file:
                json.dump([], file)

    def insert_item(self, item):
        '''
        Insert an item into the JSON file

        :param item: The item to insert
        '''
        try:
            with open(path + self.file_name, 'r+') as file:
                data = json.load(file)
                data.append(item)
                file.seek(0)
                json.dump(data, file)
            logger.debug(f"Item inserted into JSON file: {item}")
        except InvalidJSON as e:
            logger.error(f"Error inserting item into JSON file: {e}")

    def read_data(self):
        '''
        Read data from the JSON file.

        :return: List containing the data read from the file
        '''
        try:
            with open(path + self.file_name, 'r') as file:
                return json.load(file)
        except InvalidData as e:
            logger.error(f"Error reading data from JSON file: {e}")
            return []
