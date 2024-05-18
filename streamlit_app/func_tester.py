import streamlit as st
import pandas as pd

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)



st.markdown("""
<style>
.navbar-nav .nav-link {
    padding-top: 40px; /* Adjust the value as needed */
    padding-bottom: 0px; /* Adjust the value as needed */
}
.navbar-brand {
    margin-top: 40px; /* Adjust the value as needed */
    margin-bottom: 0px; /* Adjust the value as needed */
}
</style>
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #416978; height: 100px;">
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

st.markdown('''# **Comparing Skies**
A Cross-Planetary Study of **Earth**'s and **Mars**'s Atmospheric Patterns.
''')

