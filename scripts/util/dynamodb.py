import boto3

class DynamoDBClient:
    def __init__(self, table_name, region_name='ap-southeast-2'):
        self.dynamodb = boto3.resource('dynamodb', region_name=region_name)
        self.table = self.dynamodb.Table(table_name)

    def insert_item(self, item):
        self.table.put_item(Item=item)
        
    def get_team_names(self, team_info_table, key):
        team_names = []
        try:
            response = self.table.get_item(Key={'TeamName': key})
            if 'Item' in response:
                teams = response['Item']['teams']  # Assuming teams are stored under a key 'teams'
                team_names = [team['name'] for team in teams]  # Adjust depending on data structure
        except Exception as e:
            print(f"Error fetching team names: {e}")
        return team_names
