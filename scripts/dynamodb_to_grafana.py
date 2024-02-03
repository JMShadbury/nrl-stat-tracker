
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from util.logger import configure_logger
import json

logger = configure_logger("DynamoDBToGrafana")

def get_dynamodb_client():
    try:
        # Initialize a DynamoDB client
        dynamodb_client = boto3.client('dynamodb')
        return dynamodb_client
    except NoCredentialsError:
        print("Credentials not available")
        return None

def retrieve_data_from_dynamodb(dynamodb_client, table_name):
    try:
        logger.info("Retrieving data from DynamoDB")
        response = dynamodb_client.scan(TableName=table_name)
        logger.info("response: {}".format(response))
        return response['Items']
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

def transform_data_for_grafana(items):
    transformed_data = []

    for item in items:
        data_point = {key: int(value['S'].replace(',', '')) for key, value in item.items() if key != 'TeamName'}
        data_point['TeamName'] = item['TeamName']['S']
        transformed_data.append(data_point)

    return transformed_data

def export_data(data, file_name):
    if not data:
        logger.error("No data to export")
        return

    try:
        with open(file_name, 'w') as file:
            json.dump(data, file, indent=4)
        logger.info(f"Data successfully exported to {file_name}")
    except IOError as e:
        logger.error(f"IOError while exporting data to JSON: {e}")



def main():
    dynamodb_client = get_dynamodb_client()
    if not dynamodb_client:
        logger.error("Failed to initialize DynamoDB client")
        return

    f = open("data/teams", "r")
    team_names = f.read().splitlines()
    f.close()
    team_names = {team.split(":")[0]: team.split(":")[1] for team in team_names}
    
    for team_name in team_names:
        raw_data = retrieve_data_from_dynamodb(dynamodb_client, team_name)
        if raw_data:
            transformed_data = transform_data_for_grafana(raw_data)
            export_data(transformed_data, 'data/'+team_name+'.json')

if __name__ == '__main__':
    main()
