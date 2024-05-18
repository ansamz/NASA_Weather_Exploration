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




path = os.path.dirname(__file__)

#_______ Page Setup
st.set_page_config(
    page_title="NASA Weather Exploration",
    page_icon="earth_spin.gif",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load your local image
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
  <a class="navbar-brand" href="https://youtube.com/dataprofessor" target="_blank">Data Professor</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse d-flex justify-content-end" id="navbarNav">
    <ul class="navbar-nav"> 
      <li class="nav-item active">
        <a class="nav-link disabled" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://youtube.com/dataprofessor" target="_blank">Earth</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Mars</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://twitter.com/thedataprof" target="_blank">Flares</a>
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


st.title("")
col_1, col_2, col_3 = st.columns([7, 2, 1])

with col_1:
    st.title("")
    st.title("Comparing Skies ")
    st.write("A Cross-Planetary Study of Earth's and Mars's Atmospheric Patterns")

with col_2:
    st.image("images/logo_main.png", width=300)


df = pd.read_json('weather_sydney.json')

def main():
    st.title("Sydney Weather Visualization")

    selected_feature_options = ["Rain", "Temperature", "Radiation"]
    selected_feature = st.selectbox(
        "Select a Feature",
        options=selected_feature_options,
        index=selected_feature_options.index("Rain")  # Default option
    )

    feature_columns = {
        "Rain": "rain",
        "Temperature": "temperature_2m",
        "Radiation": "direct_radiation_instant"
    }

    selected_column_name = feature_columns[selected_feature]
    filtered_df = df[df[selected_column_name].notna()]

    if not filtered_df.empty:
        fig = px.line(filtered_df, x="date", y=selected_column_name, title=f"{selected_feature} Over Time")
        st.plotly_chart(fig)
    else:
        st.write(f"No data available for {selected_feature}. Please check your dataset.")


if __name__ == "__main__":
    main()


sidney_html = Image.open(path + "/sidney.html")

with open(sidney_html,'r') as f: 
    html_data = f.read()

## Show in webpage
st.components.v1.html(html_data, height = 500, scrolling = True)
