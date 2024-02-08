import boto3
from util.logger import get_logger

logger = get_logger()


class DynamoDBClient:

    def __init__(self, table_name, region_name='ap-southeast-2'):
        '''
        Initialise the DynamoDB client
        
        param table_name: The name of the DynamoDB table
        param region_name: The AWS region name
        '''
        logger.debug(
            f"Initialising DynamoDB client with table name: {table_name}")
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        logger.debug(f"DynamoDB resource: {self.dynamodb}")
        self.table = self.dynamodb.Table(table_name)
        logger.debug(f"DynamoDB table: {self.table}")
        

    def insert_item(self, item):
        '''
        Insert an item into the DynamoDB table
        
        :param item: The item to insert
        '''
        logger.info(f"Inserting item: {item}")
        self.table.put_item(Item=item)

    def get_team_names(self, team_info_table, key):
        '''
        Get the team names for a given key
        
        :param team_info_table: The name of the DynamoDB table
        :param key: The key to get the team names for
        :return: A list of team names
        '''
        logger.info(f"Getting team names for key: {key}")
        team_names = []
        try:
            response = self.table.get_item(Key={'TeamName': key})
            logger.debug(f"Response: {response}")
            if 'Item' in response:
                teams = response['Item']['teams']
                logger.debug(f"Teams: {teams}")
                team_names = [team['name'] for team in teams]
                logger.debug(f"Team names: {team_names}")
        except Exception as e:
            logger.error(f"Error fetching team names: {e}")
        return team_names
