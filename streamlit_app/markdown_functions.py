import base64
import streamlit as st

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_page_config():
    st.set_page_config(
        page_title="NASA Weather Exploration",
        page_icon="earth_spin.gif",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

def set_background_image(background_image):
    encoded_image = get_base64_of_bin_file(background_image)
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
        </style>
        """,
        unsafe_allow_html=True
    )

def set_navbar():
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

def set_global_styles():
    st.markdown("""
        <style>
            /* Your global theme styles here */
            body {
                color: white!important;
            }
            h1, h2, h3, h4, h5, h6 {
                color: white!important;
            }
            td, th {
                color: white!important;
            }
            p {
                color: black!important;
            }
            li {
                color: black!important;
            }
            a {
                color: white!important;
            }
         .navbar-brand,.navbar-nav.nav-link {
                color: blue!important;
            }
         .navbar-nav.nav-link:hover {
                color: white!important; /* Keep hover effect */
            }
            /* Targeting dropdown options within the select box */
         .stSelectbox div[data-baseweb="select"] > div[role="listbox"] > div[role="option"],
         .stSelectbox div[data-baseweb="select"] > div[role="listbox"] > div[role="option"]:hover {
                background-color: #f0f0f0; /* Change this to your desired background color */
                color: white!important; /* Ensuring text color contrasts well with the background */
            }
        </style>
    """, unsafe_allow_html=True)

def set_tab_styles():
    st.markdown(
        """
        <style>
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
                font-weight: bold;
                justify-content: flex-end;
                margin-right: 10px;
            }

            .stTabs [data-baseweb="tab"] {
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
            }

            .stTabs [aria-selected="true"] {
                background-color: rgba(229, 121, 41, 0.3);
            }
        </style>
        """,
        unsafe_allow_html=True
    )

def set_selectbox_styles():
    st.markdown(
        """
        <style>
            .stSelectbox div[data-baseweb="select"] > div:first-child {
                    background: linear-gradient(90deg, rgba(27,68,214,0.5) 0%, rgba(9,121,108,0.8) 39%, rgba(121,255,0,0.2) 100%);
                    border-color: rgba(27,68,214,0.5);
                    color: rgba(27,68,214,0.5);
                    padding: 2px;
                    border-radius: 5px;
                }
            .stSelectbox div[data-baseweb="select"] > div[role="listbox"] > div[role="option"] {
                    background-color: white!important;
                    color: white!important;
                    padding: 10px;
                    border-radius: 5px;
                }
            .stSelectbox div[data-baseweb="select"] > div[role="listbox"] > div[role="option"]:hover {
                    background-color: rgba(9,121,108,0.8); /* Ensures hover state has matching color */
                    color: #fcfcfc;
                }
        </style>
        """,
        unsafe_allow_html=True
    )
