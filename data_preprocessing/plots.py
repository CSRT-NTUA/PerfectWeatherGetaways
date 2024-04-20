import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk
import numpy as np
# Load your dataset
@st.cache_resource
def load_data():
    df = pd.read_csv('data.csv')
    df = df.drop('date', axis=1) 
    df = df.rename(columns={'temperature_2m': 'Temperature', 'relative_humidity_2m': 'Humidity', 'rain':'Rain', 'snowfall':'Snow', 'cloud_cover':'Clouds', 'wind_speed_10m':'Winds'})
    return df
def density_mapbox_plot(data, lat, lon, column):
    return px.density_mapbox(data, lat=lat, lon=lon, z=data[column], radius=10 , center=dict(lat=38, lon=24) , zoom=5 , mapbox_style="stamen-terrain")

# Main function
def histogram_plot(data):
    st.title('Histogram Plotter')

    # Define column options with emojis
    column_options = {
        'temperature_2m': 'Temperature 🌡️',
        'relative_humidity_2m': 'Humidity 💧',
        'rain': 'Rain ☔️',
        'snowfall': 'Snow ❄️',
        'cloud_cover': 'Clouds ☁️',
        'wind_speed_10m': 'Winds 💨'
    }

    # Select column
    selected_column = st.selectbox('Select a column', options=list(column_options.keys()), format_func=lambda x: column_options[x])

    # Plot histogram
    plt.figure(figsize=(20, 15))
    sns.barplot(data, x="date", y=selected_column, hue=selected_column)
    plt.title(f'Barplot of {selected_column}')
    plt.xlabel(selected_column)
    plt.ylabel(f'{selected_column}')
    st.pyplot(fig=None)

#if __name__ == '__main__':
#    st.set_option('deprecation.showPyplotGlobalUse', False)
#    data = load_data()
   