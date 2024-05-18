import boto3
import json

# Path to the JSON file with AWS credentials
config_path = '../awsconfig.json'

# Load credentials safely
try:
    with open(config_path, 'r') as jsonfile:
        data = json.load(jsonfile)
        YOUR_ACCESS_KEY = data['aws_access_key_id']
        YOUR_SECRET_KEY = data['aws_secret_access_key']
        YOUR_REGION = data['region_name']
except FileNotFoundError:
    print("Configuration file not found.")
    raise
except KeyError:
    print("Incorrect format or missing keys in configuration file.")
    raise
except json.JSONDecodeError:
    print("Error decoding JSON from configuration file.")
    raise

# Initialize AWS S3 client with credentials
try:
    s3 = boto3.client('s3',
                      aws_access_key_id=YOUR_ACCESS_KEY,
                      aws_secret_access_key=YOUR_SECRET_KEY,
                      region_name=YOUR_REGION)
except Exception as e:
    print("Failed to create S3 client:", str(e))
    raise

# Example operation to list buckets to verify connectivity
try:
    response = s3.list_buckets()
    print("Buckets:", [bucket['Name'] for bucket in response['Buckets']])
except boto3.exceptions.S3TransferFailedError as e:
    print("S3 Client Error:", str(e))
    raise
