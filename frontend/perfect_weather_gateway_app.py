import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk
import pycountry
import sys
from datetime import datetime, timedelta
sys.path.append("../api/")
sys.path.append("../data_preprocessing/")
from api import get_answer, travelmyth_api
from meteo_forecast import get_weather
from weather_preprocess_plotting import mean_implementation
from map_plot import create_map

def plot_weather_data(data, initial_lat, initial_lon):
    fig = st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=initial_lat,
        longitude=initial_lon,
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
           'HexagonLayer',
           data=data,
           get_position='[lon, lat]',
           radius=200,
           elevation_scale=4,
           elevation_range=[0, 1000],
           pickable=True,
           extruded=True,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=data,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=200,
        ),
    ],
    ))
    return fig

if 'screen' not in st.session_state:
    st.session_state.screen = "welcome_screen"
def get_flag_url(country_code):
    return f"https://flagcdn.com/32x24/{country_code.lower()}.png"

def show_results():
    st.header("Our results")
    st.components.v1.iframe("https://www.travelmyth.com/" , width=800, height=2600)
    

def show_team():
    st.header("CSRT Team")
    
    code = """
    def hello():
        print("Hello, from CSRT Team!")

    hello()
    """

    st.code(code, language='python')

def show_categories():
    hotel_type = ["Adult Only", "Boutique-Style", "Castle, Family, Haunted, Luxury, Monastery", "Skyscraper", "Small", "Spa", "Vineyard", "Treehouse", "Beachfront", "5 Star", "4 Star", "3 Star", "Cheap", "Historic"]
    sports = [
    "Ski", "Ski In Ski Out", "Yoga", "Tennis", "Golf", "Water Park", "Wave Pool", "Pool Lap Lanes",
    "Pool Swim Up Bar", "Pool Water Slide", "Rooftop Pool", "Lazy River", "Indoor Pool", "Outdoor Pool",
    "Children's Pool"]
    pets = ["Dog Friendly", "Dogs Stay Free", "Dog Play Area", "Dog Sitting"]
    entertainment = ["Honeymoon", "Nightlife", "Romantic", "Unusual", "Panoramic View Pool", "Overwater Bungalows", "Casino"]
    #health_and_safety = ["Health & Safety"]
    others = ["Parking", "All-Inclusive Packages", "Rooms with Fireplace", "Rooms with Jacuzzi / Hot-Tub",
        "EV charging stations", "Gym", "Free Wi-Fi", "Business", "Accessible", "Sustainability Journey"]
    selected_hotel_types = st.multiselect("Select Hotel Type", hotel_type)
    selected_sports = st.multiselect("Select Sports", sports)
    selected_pets = st.multiselect("Select Pets", pets)
    selected_entertainment = st.multiselect("Select Entertainment", entertainment)
    selected_health_and_safety = st.checkbox("Select Health & safety")
    selected_others = st.multiselect("Select other options", others)


"""def how_it_works():
    with open("api_test.py", 'r') as file:
        text = file.read()
    st.write("This is the api for asking info:")
    st.code(text, language='python')"""
    

def assign_score(df, weather, min_temperature, max_temperature, date_of_arrival, date_of_deperature):
    print(df.columns)
    df.reset_index(level=0, inplace=True)
    date_of_arrival = pd.to_datetime(date_of_arrival)
    date_of_deperature = pd.to_datetime(date_of_deperature)
    #df = df[df['date'] >= date_of_arrival and df['date'] <= date_of_deperature]
    csv_mintemp = df['temperature_2m'].min()
    csv_maxtemp = df['temperature_2m'].max()
    csv_stdtemp = df['temperature_2m'].std()
    csv_meantemp = df['temperature_2m'].mean()
    trip_duration = (date_of_deperature-date_of_arrival).days + 1
    csv_rain_days_percentage = len(df[df['rain'] > 0.0].index)/trip_duration
    csv_cloudy_days_percentage = len(df[df['cloud_cover'] > 0.5].index)/trip_duration
    csv_snowy_days_percentage = len(df[df['snowfall'] > 0.0].index)/trip_duration
    

    score = 0
    if min_temperature > csv_mintemp:
        score -= (min_temperature - csv_mintemp)
    else:
        score += (min_temperature-csv_mintemp)/(max_temperature-min_temperature)
    if max_temperature < csv_maxtemp:
        score -= (csv_maxtemp - max_temperature)
    else:
        score += (csv_maxtemp-max_temperature)/(max_temperature-min_temperature)
    score -= abs(csv_meantemp - (max_temperature-min_temperature)/2)/(max_temperature-min_temperature)
    score -= csv_stdtemp/(max_temperature-min_temperature)
    #weather: sunny, rainy, snow
    if weather == "sunny":
        score -= csv_rain_days_percentage
        score -= csv_cloudy_days_percentage
        score -= csv_snowy_days_percentage
    elif weather == "rainy":
        score += csv_rain_days_percentage
    elif weather == "snow":
        score += csv_snowy_days_percentage
    return score

def user_input():
    prompt = st.text_input("Enter: ")
    st.markdown("<h4 style='text-align: center;'>Add more options for your trip</h4>", unsafe_allow_html=True)

    st.markdown("#### Select dates")
    date_of_arrival = st.date_input('Date of arrival')
    date_of_deperature = st.date_input('Date of departure')
    
    st.markdown("#### Select Country")
    countries = [(country.name, country.alpha_2) for country in pycountry.countries]
    selected_country = st.multiselect("Select a country", countries, format_func=lambda x: x[0])
    #print(selected_country)
    flag_urls = []
    for country in selected_country:
        print(country[0])
        flag_urls.append(get_flag_url(country[1]))
    st.write(
        " ".join([f"<img src='{url}' width='40' style='margin-right: 10px;'>" for url in flag_urls]), 
        unsafe_allow_html=True
    )
    
    st.markdown("#### Select Weather")
    weather = st.radio('Weather:', ['Sunny','Rainy','Snow'])
    min_temperature = st.number_input('Enter minimum temperature')
    max_temperature = st.number_input('Enter maximum temperature')
    
    st.markdown("#### Select Activities")
    show_categories()
    
    if st.button('Search'):
        prompt += "Use the following instructions when answering the prompt above: Reply in Json format Include the places suggestions in an array. Suggest as many as you can, preferably at least 10. When writing, the place name includes only the name, not the country, wider region or continent. If the prompt is appropriate for any of the following categories include the category in the json: Categories: infinity_pool,heated_pool,indoor_pool,rooftop_pool,wave_pool,children_pool,panoramic_view_pool,pool_swim_up_bar,pool_water_slide,pool_lap_lanes,water_park,lazy_river,private_pool,dog_play_area,dog_sitting,dogs_stay_free,outdoor_pool,health_and_safety,treehouse,haunted,overwater_bungalows,three_star,skyscraper,four_star,five_star,yoga,tennis,small,adult_only,gym,accessible,cheap,parking,business,free_wifi,pool,nightlife,romantic,dog_friendly,family,spa,casino,honeymoon,eco_friendly,beach,beachfront,ski,ski_in_ski_out,historic,unusual,vineyard,monastery,castle,golf,luxury,boutique,ev_charging,jacuzzi_hot_tub,fireplace,all_inclusive"
        results = get_answer(prompt)
        weathers = []
        scores = {}
        points = []
        for x in results:
            points.append((x['latitude'], x['longitude']))
            current_csv = get_weather(x['latitude'], x['longitude'])
            current_csv = mean_implementation(current_csv)
            # youre ready to do the classification
            # user inputs are [weather, min_temp, max_temp, date_of_arrival, date_of_departure, selected_country]
            scores[x['name']] = assign_score(current_csv, weather, min_temperature, max_temperature, date_of_arrival, date_of_deperature)
        #st.write(weathers)
        #st.write(results)
        scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
        top_recommendation = next(iter(scores))
        container = st.container(border=True)
        for (index, x) in enumerate(scores):
            container.write(f"{index + 1}'st Recomendation : {x}")
        create_map(points[0][0], points[0][1], points)
        
if __name__ == "__main__":
    st.sidebar.header("Menu")
    st.sidebar.write("")
    if st.sidebar.button('Show results'):
        st.session_state.screen = "result"
    
    if st.sidebar.button('Team'):
        st.session_state.screen = "welcome_screen"
    if st.sidebar.button('User input'):
        st.session_state.screen = "user_input"
        
    """if st.sidebar.button('How it works?'):
        st.session_state.screen = "how_it_works" """
        
        
    if st.session_state.screen == "welcome_screen":
        show_team()
    if st.session_state.screen == "result":
        show_results()
    if st.session_state.screen == "user_input":
        user_input()
    """if st.session_state.screen == "how_it_works":
        how_it_works() """
    
    #data = pd.read_csv("../api/data.csv")
    #fig = plot_weather_data(data, )
    #print(st.session_state.screen)
