#_______ Library Import
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import plotly.express as px
from datetime import datetime
import json
import base64
from PIL import Image
import io
import os
from PIL import Image

import db_connect
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy import stats

import sqlalchemy
from sqlalchemy.sql import text
import toml

path = "C:/Users/joana/OneDrive/Desktop/HSLU/3rd_semester/DWL/NASA_Weather_Exploration/streamlit_app/images/"

#_______ Page Setup
st.set_page_config(
    page_title="NASA Weather Exploration",
    page_icon="earth_spin.gif",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


background_image = "images/background.jpg"
encoded_image = get_base64_of_bin_file(background_image)

st.markdown("""
        <style>
               .block-container {
                    padding-top: 1rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)


st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<style>
.navbar-nav .nav-link {
    padding-top: 40px; 
    padding-bottom: 0px; 
    color: black !important;
}
.navbar-brand {
    margin-top: 40px; 
    margin-bottom: 0px; 
    color: black !important;
}
.navbar-nav .nav-link:hover {
    color: white !important; /* Change font color on hover */
}
</style>
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background: linear-gradient(90deg, rgba(27,68,214,0.5) 0%, rgba(9,121,108,0.8) 39%, rgba(121,255,0,0.2) 100%); height: 100px;">
  <a class="navbar-brand" href="/home">Data Warehouse and Data Lake Systems</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarNav">
    <ul class="navbar-nav"> 
      <li class="nav-item active">
        <a class="nav-link disabled" href="/home">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Earth_Weather">Earth</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Mars_Weather">Mars</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="/Solar_Flares">Flares</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)


st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url('data:image/jpg;base64,{encoded_image}');
            background-size: cover;
        }}

        /* Remove padding from the body */
        body {{
            padding-top: 20px;
            margin-top: 0;
        }}

        /* Remove padding from the Streamlit root element */
        .stApp {{
            padding-top: 20px;
            margin-top: 0;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 10px;
            font-weight: bold;
            justify-content: flex-end;
            margin-right: 10px;
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 35px;
            white-space: pre-wrap;
            background-color: rgba(34, 128, 172, 0.25);
            border-radius: 4px 4px 0px 0px;
            gap: 3px;
            padding-top: 0px;
            padding-bottom: 10px;
            padding-left: 10px;
            padding-right: 10px;
            color: #143066;
            font-weight: bold;
        }}

        .stTabs [aria-selected="true"] {{
            background-color: rgba(229, 121, 41, 0.3);
        }}
    </style>
    """,
    unsafe_allow_html=True
)

#__________________________________________________________

earth_weather_data = db_connect.earth_weather_data()
daily_average = earth_weather_data.groupby('date').agg({
    "latitude" : "first",
    "longitude" : "first",
    "temperature_2m" : "mean",
    "relative_humidity" : "mean",
    "rain" : "mean", 
    "direct_radiation_instant" : "mean",
    "location" : "first" 
}).reset_index()


locations = ["Amazon", "Athens", "Death Valley", "Everest", "London", "McMurdo", "Oymyakon", "Sahara", "Serengeti", "Sydney", "Zurich", ]

st.title("Weather Visualization")

if locations:
    selected_location = st.selectbox(
        "Select a Location",
        options = locations,
        index=0
    )

    selected_feature_options = ["Rain", "Temperature", "Radiation"]
    selected_feature = st.selectbox(
        "Select a Feature",
        options=selected_feature_options,
        index = selected_feature_options.index("Rain")  # Default option
    )

    feature_columns = {
        "Rain": "rain",
        "Temperature": "temperature_2m",
        "Radiation": "direct_radiation_instant"
    }

    selected_column_name = feature_columns[selected_feature]
    filtered_df = daily_average[daily_average[selected_column_name].notna()]

    if not filtered_df.empty:
        fig = px.line(filtered_df, x="date", y=selected_column_name, title=f"{selected_feature} Over Time in {selected_location}")
        st.plotly_chart(fig)
    else:
        st.write(f"No data available for {selected_feature} in {selected_location}. Please check your dataset.")
else:
    st.write("No locations found in the database.")