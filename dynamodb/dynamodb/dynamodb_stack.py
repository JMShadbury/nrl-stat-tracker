from aws_cdk import (
    aws_dynamodb as dynamodb,
    Stack,
    App,
    aws_lambda as lambda_,
    BundlingOptions,
    Duration
)
from constructs import Construct   

class DynamodbStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get Teams from file
        f = open("../data/teams", "r")
        teams = f.read().splitlines()
        f.close()

        # Create a dictionary of teams
        teams = {team.split(":")[0]: team.split(":")[1] for team in teams}

        # Create a table for each team
        for team in teams:
            team_id = teams[team]
            current_team = dynamodb.Table(
                self, f"{team}Table",
                table_name=team,
                partition_key=dynamodb.Attribute(
                    name="TeamName",
                    type=dynamodb.AttributeType.STRING
                ),
                read_capacity=5,
                write_capacity=5
            )

        # Ladder Table
        ladder = dynamodb.Table(
            self, "LadderTable",
            table_name="Ladder",
            partition_key=dynamodb.Attribute(
                name="TeamName",
                type=dynamodb.AttributeType.STRING
            ),
            read_capacity=5,
            write_capacity=5
        )