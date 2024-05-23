#_______ Library Import
import streamlit as st
import base64
import markdown_functions as md
import os

path = "./images/"

# st.write(os.getcwd())
# checking if the current working directory is correct 
if os.getcwd()[-3:] == "src":
    os.chdir('.')
# st.write(os.getcwd())

#_______ Page Setup
st.set_page_config(
    page_title="NASA Weather Exploration",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


background_image = os.path.join(path, "background.jpg")
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

st.markdown(md.get_navbar_markdown(), unsafe_allow_html=True)
st.markdown(md.background_and_tabs_styles(encoded_image), unsafe_allow_html = True)


st.write("")
st.title("")
col_1, col_2, col_3 = st.columns([7, 2, 1])

with col_1:
    st.title("")
    st.title("**Comparing Skies**")
    st.subheader("A Cross-Planetary Study of Earth's and Mars's Atmospheric Patterns")

with col_2:
    st.title("")
    st.image("./images/logo_cs.png", width=350)


st.title("")
st.title("")
st.write("")
st.write("")
st.write("Welcome to Compare-Skies!")
st.write("""We are a group of space enthusiasts that couldn't find relevant information on Earth's and Mars' weather and decided it was time to take action.
         We rolled our sleeves and set out to compile in an easy and accessible way the information needed to understand if Mars can be a potential habitat 
         in the event of a catastrophy that rules out Earth as our home. 
         """)

st.write("""
        Here, we provide the scientific and general community a central source of data. Furthermore, our team also performs data analysis and shares the resulting insights.    
""")

st.write("""
        So, join us in our journey of exploration. The ride is about to get heated!  🔥   
""")

