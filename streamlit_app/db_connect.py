import sqlalchemy
from sqlalchemy.sql import text
import toml
import pandas as pd

# Load database credentials from secrets.toml
config = toml.load("config\secrets.toml")
db_config = config['database']

# Create the database URL
database_url = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['db_name']}"

# Create an engine
engine = sqlalchemy.create_engine(database_url)

def weather_data_location(city_name):
    try:
        with engine.connect() as connection:
            print("Successfully connected to the database!")
            result = pd.read_sql_query(f"SELECT * FROM weather_data WHERE location = '{city_name}';", connection)
            return result
    except Exception as e:
        print(f"An error occurred: {e}")
