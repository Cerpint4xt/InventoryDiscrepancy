import streamlit as st
import pandas as pd
import numpy as np


st.title(':bar_chart: Inventory Discrepancy')

DATA_URL_expected = ("https://storage.googleapis.com/mojix-devops-wildfire-bucket/analytics/bootcamp_2_0/Bootcamp_DataAnalysis_Expected.csv")

DATA_URL_counted = ("https://storage.googleapis.com/mojix-devops-wildfire-bucket/analytics/bootcamp_2_0/Bootcamp_DataAnalysis_Counted.csv")

@st.cache
def load_data(url):
    data = pd.read_csv(url, encoding="latin-1", dtype=str)
    return data

with st.spinner(text='In progress'):
    data_expected = load_data(DATA_URL_expected)
    time.sleep(5)
    st.success("Done! df_expected loaded!")

with st.spinner(text='In progress'):
    data_expected = load_data(DATA_URL_counted)
    time.sleep(5)
    st.success("Done! df_expected loaded!")
'''
data_load_state = st.text('Loading data...')

data_load_state.text("Done! df_expected loaded! (using st.cache)")

data_load_state = st.text('Loading data...')
data_counted = load_data(DATA_URL_counted)
data_load_state.text("Done! df_counted loaded! (using st.cache)")
'''
if st.checkbox('Show raw data expected'):
    st.subheader('Raw data expected')
    st.write(data_expected)

if st.checkbox('Show raw data counted'):
    st.subheader('Raw data counted')
    st.write(data_counted)

st.markdown('---')
