import boto3

class DynamoDBClient:
    def __init__(self, table_name, region_name='ap-southeast-2'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def insert_item(self, item):
        self.table.put_item(Item=item)
