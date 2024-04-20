import pandas as pd
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import sys
sys.path.append("../api/")
from meteo_forecast import get_weather

def mean_implementation(df):
    df["date"] = df['date'].apply(extract_day)
    columns = ["temperature_2m","relative_humidity_2m","rain","snowfall","cloud_cover","wind_speed_10m"]
    return df.groupby(df['date'])[columns].mean()

def extract_day(date_string):
    return str(date_string)[:10]

"""def average_temp_per_date(df,column):
    df['date'] = df['date'].apply(lambda x: extract_day(x))
    avg_by_date = df.groupby(df['date'])[column].mean()
    return avg_by_date"""

def meteo_temperature_print(df, columns):
    #df['date'] = df['date'].apply(lambda x: extract_day(x))
    for column in columns:
        #df = average_temp_per_date(df,column)
        st.line_chart(df['date'], df[column])
   
if __name__ == "__main__":
    # weather = pd.read_csv("../api/data.csv")
    # print(get_weather(1.62131, 52.2313123))
    weather = get_weather(1.721341, 52.51241) # data frame
    df_mean = mean_implementation(weather)
    print(df_mean)