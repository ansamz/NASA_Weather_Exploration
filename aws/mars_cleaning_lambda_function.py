import boto3
import pandas as pd
import os
from io import StringIO

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    # Get the bucket name and key from the event (assuming an S3 trigger)
    bucket = os.environ['BUCKET_NAME']
    key = "weather_mars_combined.csv"
    
    try:
        # Read the CSV data from S3
        response = s3_client.get_object(Bucket=bucket, Key=key)
        csv_data = response['Body'].read().decode('utf-8')
        # https://dwlproject-marsweatherdata.s3.amazonaws.com/weather_mars_combined.csv
        
        # Create a DataFrame
        df = pd.read_csv(StringIO(csv_data))
        print(df.head(5))
        print(df.columns)
    
        # Clean the data (remove rows with NaN values)
        df.drop(columns='wind_speed', inplace=True)
        df.dropna(subset=['min_temp','max_temp','pressure'], how='all', inplace=True)
            
        print(df.info())
        # Convert the DataFrame back to CSV
        csv_cleaned = df.to_csv(index=False)
    
        # Write the cleaned data back to S3
        output_key = "cleaned/" + key  # Save to a different location to avoid overwriting
        s3_client.put_object(Bucket=bucket, Key=output_key, Body=csv_cleaned)
    
            
        return {
            'statusCode': 200,
            # 'body': 'Data read into csv'
            'body': 'Data cleaned and saved to {}'.format(output_key)
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'body': str(e)
        }