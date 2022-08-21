import streamlit as st
import pandas as pd
import numpy as np
import time


pd.set_option('display.precision', 1)


st.title(':bar_chart: Inventory Discrepancy')

DATA_URL_expected = ("https://storage.googleapis.com/mojix-devops-wildfire-bucket/analytics/bootcamp_2_0/Bootcamp_DataAnalysis_Expected.csv")

DATA_URL_counted = ("https://storage.googleapis.com/mojix-devops-wildfire-bucket/analytics/bootcamp_2_0/Bootcamp_DataAnalysis_Counted.csv")

def load_data(url):
    with st.spinner(text='In progress'):
        data = pd.read_csv(url, encoding="latin-1", dtype=str)
        time.sleep(2)
        st.success(f"Done! CSV: {url} loaded!")
    return data

st.markdown('---')

data_expected = load_data(DATA_URL_expected)
data_counted = load_data(DATA_URL_counted)

if st.checkbox('Show raw data expected'):
    st.subheader('Raw data expected')
    st.write(data_expected)

if st.checkbox('Show raw data counted'):
    st.subheader('Raw data counted')
    st.write(data_counted)

st.markdown('---')

df_counted = data_counted
df_counted = df_counted.drop_duplicates('RFID')
df_B = df_counted.groupby("Retail_Product_SKU").count()[["RFID"]].reset_index().rename(columns={"RFID":"Retail_CCQTY"})

my_col_selected = ["Retail_Product_Name",
                   "Retail_Product_SKU",
                   "Retail_Product_Size",
                   "Retail_Product_Style",
                   "Retail_Product_Color",
                   "Retail_SOHQTY"]

df_expected = data_expected
df_A = df_expected[my_col_selected]


df_discrepancy = pd.merge(df_A, df_B, how="outer", left_on="Retail_Product_SKU", right_on="Retail_Product_SKU", indicator=True)
df_discrepancy['Retail_CCQTY'] = df_discrepancy['Retail_CCQTY'].fillna(0).astype(int)
df_discrepancy["Retail_SOHQTY"] = df_discrepancy["Retail_SOHQTY"].fillna(0).astype(int)

df_discrepancy.loc[df_discrepancy["Retail_SOHQTY"] == df_discrepancy["Retail_CCQTY"], "Match"] = 1
df_discrepancy["Match"] = df_discrepancy["Match"].fillna(0).astype(int)
df_discrepancy["Diff"] = df_discrepancy["Retail_CCQTY"] - df_discrepancy["Retail_SOHQTY"]
df_discrepancy.loc[df_discrepancy["Diff"]<0, "Unders"] = df_discrepancy["Diff"] * (-1)
df_discrepancy["Unders"] = df_discrepancy["Unders"].fillna(0).astype(int)
df_discrepancy.loc[df_discrepancy["Diff"]>0, "Overs"] = df_discrepancy["Diff"]
df_discrepancy["Overs"] = df_discrepancy["Overs"].fillna(0).astype(int)
df_discrepancy_enriched = df_discrepancy.groupby("Retail_Product_Name").sum()


if st.checkbox('Show data frame Discrepancy'):
    st.subheader('Data discrepancy with Match, Unders, Overs')
    st.write(df_discrepancy_enriched)

df_discrepancy["SKUAccuracy"] = (df_discrepancy["Match"] / df_discrepancy["Retail_SOHQTY"]) * 100
df_discrepancy["SKUAccuracy"].replace([np.inf, -np.inf], np.nan, inplace=True)
df_discrepancy["SKUAccuracy"] = df_discrepancy["SKUAccuracy"].fillna(0)

df_discrepancy["ItemAccuracy"] = (df_discrepancy["Retail_CCQTY"] / df_discrepancy["Retail_SOHQTY"]) * 100
df_discrepancy["ItemAccuracy"].replace([np.inf, -np.inf], np.nan, inplace=True)
df_discrepancy["ItemAccuracy"] = df_discrepancy["ItemAccuracy"].fillna(0)

df_discrepancy["UnitLevelAccuracy"] = ((df_discrepancy["Retail_SOHQTY"] - df_discrepancy["Unders"] - df_discrepancy["Overs"]) / df_discrepancy["Retail_SOHQTY"]) * 100
df_discrepancy["UnitLevelAccuracy"].replace([np.inf, -np.inf], np.nan, inplace=True)
df_discrepancy["UnitLevelAccuracy"] = df_discrepancy["UnitLevelAccuracy"].fillna(0)


st.markdown('---')
if st.checkbox('Show data frame Discrepancy with Accuracy Calculation'):
    st.subheader('Data discrepancy with Match, Unders, Overs, SKUAccuracy, ItemAccuracy, UnitLevelAccuracy')
    st.dataframe(df_discrepancy.groupby("Retail_Product_Name").sum())

st.markdown('---')

df_discrepancy_plot = df_discrepancy.groupby("Retail_Product_Name").sum()
df_discrepancy_plot = df_discrepancy_plot[['Diff','Unders', 'Overs', 'Match']]
st.bar_chart(df_discrepancy_plot)

st. bar_chart(f_discrepancy_plot.plot.barh(stacked=True))








