import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Load your dataset
@st.cache_resource
def load_data():
    df = pd.read_csv('../api/data.csv')
    return df

# Main function
def main():
    st.title('Histogram Plotter')

    # Load the dataset
    data = load_data()
    data = data.drop('date', axis=1) 
    data = data.rename(columns={'temperature_2m': 'Temperature', 'relative_humidity_2m': 'Humidity', 'rain':'Rain', 'snowfall':'Snow', 'cloud_cover':'Clouds', 'wind_speed_10m':'Winds'})
    # Define column options with emojis
    column_options = {
        'Temperature': 'Temperature 🌡️',
        'Humidity': 'Humidity 💧',
        'Rain': 'Rain ☔️',
        'Snow': 'Snow ❄️',
        'Clouds': 'Clouds ☁️',
        'Winds': 'Winds 💨'
    }

    # Select column
    selected_column = st.selectbox('Select a column', options=list(column_options.keys()), format_func=lambda x: column_options[x])
  
    # Plot histogram
    plt.figure(figsize=(8, 6))
    sns.histplot(data[selected_column], kde=True)
    plt.title(f'Histogram of {selected_column}')
    plt.xlabel(selected_column)
    plt.ylabel('Frequency')
    st.pyplot(fig=None)

if __name__ == '__main__':
    st.set_option('deprecation.showPyplotGlobalUse', False)
    main()
