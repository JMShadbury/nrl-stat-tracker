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
        
    def fetch_data_from_dynamodb(self, table_name):
        '''
        Fetch data from a DynamoDB table.
        '''
        try:
            client = boto3.client('dynamodb')
            logger.info(f"Retrieving data from DynamoDB table: {table_name}")
            return client.scan(TableName=table_name)['Items']
        except Exception as e:
            logger.error(f"Error fetching data from DynamoDB: {e}")
            return None
