import streamlit as st
import pandas as pd
import numpy as np
import time


st.title(':bar_chart: Inventory Discrepancy')

DATA_URL_expected = ("https://storage.googleapis.com/mojix-devops-wildfire-bucket/analytics/bootcamp_2_0/Bootcamp_DataAnalysis_Expected.csv")

DATA_URL_counted = ("https://storage.googleapis.com/mojix-devops-wildfire-bucket/analytics/bootcamp_2_0/Bootcamp_DataAnalysis_Counted.csv")

@st.cache
def load_data(url):
    with st.spinner(text='In progress'):
        data = pd.read_csv(url, encoding="latin-1", dtype=str)
        time.sleep(2)
        st.success("Done! loaded!")
    return data

data_expected = load_data(DATA_URL_expected)
data_counted = load_data(DATA_URL_counted)

if st.checkbox('Show raw data expected'):
    st.subheader('Raw data expected')
    st.write(data_expected)

if st.checkbox('Show raw data counted'):
    st.subheader('Raw data counted')
    st.write(data_counted)

st.markdown('---')
