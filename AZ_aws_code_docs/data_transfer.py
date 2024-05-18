# Install libraries in the pythong environemnt created
# pip install boto3 psycopg2-binary sqlalchemy
# I am using psycopg2 or sqlalchemy to establish a connection to your Aurora database

import boto3 # access the data
import pandas as pd
import json
from sqlalchemy import create_engine
import os

# ------------------------------------------------------
# preprocessing functions

def process_flare_data(df):
    print(df.head())
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
        print(df.head())
    # Convert date fields to datetime
    df['beginTime'] = pd.to_datetime(df['beginTime'], format='%Y-%m-%dT%H:%MZ', errors='coerce')
    df['endTime'] = pd.to_datetime(df['endTime'], format='%Y-%m-%dT%H:%MZ', errors='coerce')

    # Map flare classes to intensity descriptions
    flare_intensity = {
        'X': 'Most intense',
        'M': 'Medium',
        'C': 'Small',
        'B': 'Very Small',
        'A': 'Smallest'
    }
    df['intensity'] = df['classType'].str[0].map(flare_intensity)
    print('columns:')
    print(df.columns)
    return df.reset_index(drop=True)

def process_kaggle_data(df):
    df.drop(columns='wind_speed', inplace=True)
    df.dropna(subset=['min_temp','max_temp','pressure'], how='all', inplace=True)
    df['terrestrial_date'] = pd.to_datetime(df['terrestrial_date'])
    if 'season' in df.columns:
        df = df.rename(columns={'season': 'month'})
    df = df.drop(columns=['index'])
    print(df.head())
    return df.reset_index(drop=True)

def process_meteo_data(json, file_name):
    df_weather_data = pd.DataFrame(json)
    df_weather_data['location'] = file_name.split('.json')[0].split('_')[-1]
    df_weather_data = df_weather_data.dropna()
    df_weather_data['date'] = pd.to_datetime(df_weather_data['date'], unit='ms')
    return df_weather_data.reset_index(drop=True)
# ------------------------------------------------------

# put aws credintials in a json file and read them
with open('../awsconfig.json', 'r') as jsonfile:
    data = json.load(jsonfile)
YOUR_ACCESS_KEY = data['aws_access_key_id']
YOUR_SECRET_KEY = data['aws_secret_access_key']
YOUR_REGION = data['region_name']
SESSION_TOKEN = data['aws_session_token']

# AWS credentials
s3 = boto3.client('s3',
                  region_name = YOUR_REGION,
                  aws_access_key_id = YOUR_ACCESS_KEY,
                  aws_secret_access_key = YOUR_SECRET_KEY,
                  aws_session_token = SESSION_TOKEN
                  )

# bucket names
buckets = ['meteoswissdata'] # 'marskaggledata', 'solarflaredata', 

# Connect to Aurora PostgreSQL
# how to write it: engine = create_engine('postgresql+psycopg2://username:password@host:port/database')
# for security reasons it's added to the config file
engine_conn = data['engine_conn']
engine = create_engine(engine_conn)

for bucket in buckets:
    if bucket == 'solarflaredata':
        response = s3.list_objects_v2(Bucket=bucket)
        files = [file['Key'] for file in response.get('Contents', []) if file['Key'].endswith('.csv')]

        for file_key in files:
            obj = s3.get_object(Bucket=bucket, Key=file_key)
            data = pd.read_csv(obj['Body'])
            print("Initial Data Loaded into DataFrame:")
            print(data.head())
            processed_data = process_flare_data(data)
            processed_data.columns = [column.lower() for column in processed_data.columns]
            # Load processed data into the database
            processed_data.to_sql('solar_flare_data', con=engine, if_exists='append', index=False)
            print(f"Data from {file_key} in {bucket} processed and loaded into database.")

    elif bucket == 'marskaggledata':
        response = s3.list_objects_v2(Bucket=bucket)
        files = [file['Key'] for file in response.get('Contents', []) if file['Key'].endswith('.csv')]

        data_frames = []

        for file_key in files:
            obj = s3.get_object(Bucket=bucket, Key=file_key)
            data = pd.read_csv(obj['Body'])
            processed_data = process_kaggle_data(data)
            data_frames.append(data)

        concatenated_df = pd.concat(data_frames, ignore_index=True)
        concatenated_df = concatenated_df.drop(columns=['index'])
        if 'season' in concatenated_df.columns:
            concatenated_df = concatenated_df.drop(columns=['season'])
        cleaned_data = concatenated_df.drop_duplicates().reset_index(drop=True)
        cleaned_data.to_sql('mars_weather', con=engine, if_exists='append', index=False)
        print(f"Data from {file_key} in {bucket} processed and loaded into database.")

    elif bucket == 'meteoswissdata':
        response = s3.list_objects_v2(Bucket=bucket)
        files = [file['Key'] for file in response.get('Contents', []) if file['Key'].endswith('.json')]

        for file_key in files:
            obj = s3.get_object(Bucket=bucket, Key=file_key)
            json_data = json.loads(obj['Body'].read().decode('utf-8'))
            processed_data = process_meteo_data(json_data, file_key) 
            processed_data.to_sql('weather_data', con=engine, if_exists='append', index=False)
            print(f"Data from {file_key} in {bucket} processed and loaded into database.")

