import json
import openmeteo_requests         # Open-Meteo weather API
import requests_cache             # chaching responses to reduce repetitive requests
import pandas as pd
from datetime import datetime, timezone, timedelta
import time
from retry_requests import retry
import boto3


s3 = boto3.client('s3')


def lambda_handler(event, context):
    openmeteo = openmeteo_requests.Client()
    coordinates = [
     {"latitude": event["latitude"], "longitude": event["longitude"]} 
    ]
    url = "https://archive-api.open-meteo.com/v1/archive"
    
    now_utc = datetime.now(timezone.utc)
    
    end_date = now_utc.strftime("%Y-%m-%d")
    
    start_date = (now_utc - timedelta(days=1)).strftime("%Y-%m-%d")
    
    base_params = {
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m", "rain", "direct_radiation_instant"]
    }
    
    results = []
    
    for coords in coordinates:
        params = base_params.copy() 
        params["latitude"] = coords["latitude"]
        params["longitude"] = coords["longitude"]
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        hourly = response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
        hourly_rain = hourly.Variables(2).ValuesAsNumpy()
        hourly_direct_radiation_instant = hourly.Variables(3).ValuesAsNumpy()
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ).strftime('%Y-%m-%d %H:%M:%S').tolist(),  # Convert DatetimeIndex to strings
            "latitude": params["latitude"],
            "longitude": params["longitude"],
            "temperature_2m": hourly_temperature_2m.tolist(),
            "relative_humidity_2m": hourly_relative_humidity_2m.tolist(),
            "rain": hourly_rain.tolist(),
            "direct_radiation_instant": hourly_direct_radiation_instant.tolist()
        }
        results.append({
            "coordinates": coords,
            "weather_data": hourly_data
        })
    results_json = json.dumps(results)
    
    obj_name = "weather_data_" + event["city"].lower() + ".json"
    
    bucket_name = "openmeteo-bucket"
    object_key = obj_name
    s3.put_object(Body=results_json, Bucket=bucket_name, Key=object_key)
    print("Data saved to S3 bucket successfully")
    return {
        'statusCode': 200,
        'body': json.dumps('Data saved to S3 bucket successfully')
    }