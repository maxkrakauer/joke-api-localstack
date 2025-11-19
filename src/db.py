import os
import boto3

JOKES_TABLE = os.environ.get("JOKES_TABLE", "Jokes")
# DYNAMODB_ENDPOINT = os.environ.get("DYNAMODB_ENDPOINT")  # set this in local dev

def get_table():
    #session = boto3.Session()
    dynamodb = boto3.resource(
        "dynamodb",
        # endpoint_url=DYNAMODB_ENDPOINT,
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
    return dynamodb.Table(JOKES_TABLE)
