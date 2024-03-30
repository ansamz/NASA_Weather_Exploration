#____ Library Import ____
import openmeteo_requests         # Open-Meteo weather API
import requests_cache             # chaching responses to reduce repetitive requests
import pandas as pd
from retry_requests import retry
import json


#____ Caching & Client____

cache_session = requests_cache.CachedSession(".cache", expire_after = -1)   # caching object; doesn't expire (-1)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)     # in case the request fails
openmeteo = openmeteo_requests.Client(session = retry_session)              # Open-Meteo client



#____ Setup ____
url = "https://archive-api.open-meteo.com/v1/archive"       # base URL

# params contains the query details 
params = {
	"latitude": 52.52,
	"longitude": 13.41,
	"start_date": "2024-03-02",
	"end_date": "2024-03-16",
	"hourly": ["temperature_2m", "relative_humidity_2m", "rain", "direct_radiation_instant"]
}


#____ Request ____
responses = openmeteo.weather_api(url, params=params)


#____ Printing responses 
response = responses[0]
print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
print(f"Elevation {response.Elevation()} m asl")
print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


hourly = response.Hourly()
hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
hourly_rain = hourly.Variables(2).ValuesAsNumpy()
hourly_direct_radiation_instant = hourly.Variables(3).ValuesAsNumpy()

hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
)}
hourly_data["temperature_2m"] = hourly_temperature_2m
hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
hourly_data["rain"] = hourly_rain
hourly_data["direct_radiation_instant"] = hourly_direct_radiation_instant

hourly_dataframe = pd.DataFrame(data = hourly_data)
print(hourly_dataframe)



#____ JSON Prep and Save
hourly_data_list = hourly_dataframe.to_dict("records")

# needed to convert the Timestamps to strings
for record in hourly_data_list:
    record["date"] = record["date"].strftime("%Y-%m-%d %H:%M:%S")  


with open("weather_data.json", "w") as outfile:
    json.dump(hourly_data_list, outfile, indent=4) 