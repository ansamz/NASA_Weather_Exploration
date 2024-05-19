import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import logging
import boto3
import os

# Initialize S3 client
s3 = boto3.client('s3')

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    api_key = os.environ['API_KEY']
    bucket_name = os.environ['BUCKET_NAME']

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    solar_flare_url = f'https://api.nasa.gov/DONKI/FLR?startDate={start_date_str}&endDate={end_date_str}&api_key={api_key}'
    
    try:
        response = requests.get(solar_flare_url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()
        
        # Process and save data
        if data:
            normalized_data = pd.json_normalize(data)
            file_name = f"solar_data_{start_date_str}_to_{end_date_str}.csv"
            file_path = f"/tmp/{file_name}"
            normalized_data.to_csv(file_path, index=False)
            
            # Upload to S3
            s3.upload_file(file_path, 'solarflaredata', file_name)
            logger.info(f"Data saved to S3 successfully, number of entries: {len(data)}")
        else:
            logger.info("No data available for the given date range.")
            
        return {
            'statusCode': 200,
            'body': json.dumps('Data processing and saving successful!')
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps('Data processing failed!')
        }