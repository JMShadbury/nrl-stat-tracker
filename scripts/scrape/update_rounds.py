import json
from util.dynamodb import DynamoDBClient
from util.defaults import Url
from teams.stats import Stats
from util.logger import configure_logger

try:
    logger = configure_logger("UpdateTeams")
    logger.setLevel("DEBUG")

    def create_stat_instance(url, stat_name):
        return Stats(url, stat_name)
    
    stats_instances = {}
    
    count = 1
    while count < 28:
        try:
            stats_instances["Round {}".format(count)] = create_stat_instance(Url.get_draw_url(count), "Round {}".format(count))
            count += 1
        except Exception as e:
            logger.error(f"Error creating instance for Round {count}: {e}", exc_info=True)
            break

    logger.info("Updating Round {count} data")
    
    all_data = {stat_name: instance.get_all_match_data()
                for stat_name, instance in stats_instances.items()}
    
    print(all_data)
    
#     try:
#         logger.info(f"Processing Round {count} data")
#         #db_client = DynamoDBClient(team_name)

#         processed_data = {stat_name: instance.process_teams_data(
#             all_data[stat_name], team_name) for stat_name, instance in stats_instances.items()}
#         if all(
#             team_name.replace(" ", "") == (data['TeamName'].replace(
#                 " ", "") if data and 'TeamName' in data else "")
#             for data in processed_data.values() if data and 'TeamName' in data
#         ):

#             # Filter out None values from processed_data
#             filtered_processed_data = {
#                 k: v for k, v in processed_data.items() if v is not None}

#             # Create the merged_data dictionary
#             merged_data = {key: value for d in filtered_processed_data.values()
#                             for key, value in d.items()}

#             logger.info(
#                 f"Merged data for {team_name}: {json.dumps(merged_data, indent=2)}")
#             if merged_data:
#                 logger.info(f"Inserting {team_name} into DynamoDB")
#                 db_client.insert_item(merged_data)
#             else:
#                 logger.debug(f"No data found for {team_name}")
#         else:
#             logger.debug(f"Team name mismatch for {team_name}")
#     except Exception as e:
#         logger.error(f"Error processing {team_name}: {e}", exc_info=True)
    
    
    
#     # Define table schema
#     table_name = 'NRLRound{count}'
#     key_schema = [
#         {
#             'AttributeName': 'Round',  # Primary key name
#             'KeyType': 'N'  # Partition key
#         }
#     ]
#     attribute_definitions = [
#         {
#             'AttributeName': 'id',
#             'AttributeType': 'N'  # 'S' for string, 'N' for number, 'B' for binary
#         }
#     ]
#     provisioned_throughput = {
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }

#     # Create the table
#     table = DynamoDBClient.create_table(table_name, key_schema, attribute_definitions, provisioned_throughput)

#     all_data = {stat_name: instance.get_all_data()
#                 for stat_name, instance in stats_instances.items()}

except Exception as e:
    logger.error(f"An error occurred: {e}")
    raise e
