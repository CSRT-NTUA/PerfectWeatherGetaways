import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk
import pycountry
import sys
from datetime import datetime, timedelta
sys.path.append("../api/")
sys.path.append("../data_preprocessing/")
from plots import histogram_plot
from api import get_answer, travelmyth_api
from meteo_forecast import get_weather
from weather_preprocess_plotting import mean_implementation
from map_plot import create_map
import time
import plotly.graph_objects as go
st.set_option('deprecation.showPyplotGlobalUse', False)


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


if 'best_csv' not in st.session_state:
    st.session_state.best_csv = pd.DataFrame()
if 'screen' not in st.session_state:
    st.session_state.screen = "welcome_screen"
if 'recommented_url' not in st.session_state:
    st.session_state.recommented_url = "https://www.travelmyth.com"
def get_flag_url(country_code):
    return f"https://flagcdn.com/32x24/{country_code.lower()}.png"

def show_results():
    st.header("Our results")
    print(st.session_state.recommented_url)
    st.components.v1.iframe(st.session_state.recommented_url , width=800, height=2600)
    

def show_team():
    st.header("CSRT Team")
    
    code = """
    def hello():
        print("Hello, we are the CSRT-NTUA Team!")
        members = []
        members.append("Spiros Maggioros")
        members.append("Konstantinos Kritharidis")
        members.append("Kostas Tziapouras")
        members.append("Nikos Tsalkitzis")
        members.append("Dimitris Minagias)
    """
    st.code(code, language='python')
    st.image('../assets/logo.png', width=300)


def typewriter(text: str, speed: int):
    tokens = text.split()
    container = st.empty()
    for index in range(len(tokens) + 1):
        curr_full_text = " ".join(tokens[:index])
        container.markdown(curr_full_text)
        time.sleep(1 / speed)

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
    return [selected_hotel_types, selected_sports, selected_pets, selected_entertainment, selected_health_and_safety, selected_others]

#def how_it_works():
#    with open("api_test.py", 'r') as file:
#        text = file.read()
#    st.write("This is the api for asking info:")
#    st.code(text, language='python')
    

def assign_score(df, weather, min_temperature, max_temperature, date_of_arrival, date_of_deperature):
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
    st.title("Perfect Weather Gateway")
    st.image('../assets/images/travelsmyth_logo.png')


    prompt = st.text_input("Enter your trip: ")
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
    categories = show_categories()
    
    if st.button('Search'):
        with st.spinner(text='In progress'):
            preferred_countries = ""
            for country in selected_country:
                preferred_countries += country[0]
                preferred_countries += ", "
            if len(preferred_countries) > 0:
                prompt += f"\n Countries that we prefer to go are {preferred_countries}. \n"
            prompt += "Use the following instructions when answering the prompt above: Reply in Json format Include the places suggestions in an array. Suggest as many as you can, preferably at least 10. When writing, the place name includes only the name, not the country, wider region or continent. If the prompt is appropriate for any of the following categories include the category in the json: Categories: infinity_pool,heated_pool,indoor_pool,rooftop_pool,wave_pool,children_pool,panoramic_view_pool,pool_swim_up_bar,pool_water_slide,pool_lap_lanes,water_park,lazy_river,private_pool,dog_play_area,dog_sitting,dogs_stay_free,outdoor_pool,health_and_safety,treehouse,haunted,overwater_bungalows,three_star,skyscraper,four_star,five_star,yoga,tennis,small,adult_only,gym,accessible,cheap,parking,business,free_wifi,pool,nightlife,romantic,dog_friendly,family,spa,casino,honeymoon,eco_friendly,beach,beachfront,ski,ski_in_ski_out,historic,unusual,vineyard,monastery,castle,golf,luxury,boutique,ev_charging,jacuzzi_hot_tub,fireplace,all_inclusive"
            results = get_answer(prompt, categories)
            scores = {}
            url = {}
            best_csv = {}
            points = [] 
            for x in results:
                points.append((x['latitude'], x['longitude']))
                current_csv = get_weather(x['latitude'], x['longitude'])
                current_csv = mean_implementation(current_csv)
                # youre ready to do the classification
                # user inputs are [weather, min_temp, max_temp, date_of_arrival, date_of_departure, selected_country]
                scores[x['name']] = assign_score(current_csv, weather, min_temperature, max_temperature, date_of_arrival, date_of_deperature)
                x['url'] += f"&checkin_day={date_of_arrival.day}&checkin_month={date_of_arrival.month}&checkin_year={date_of_arrival.year}&checkout_day={date_of_deperature.day}&checkout_month={date_of_deperature.month}&checkout_year={date_of_deperature.year}"
                url[x['name']] = x['url']
                best_csv[x['name']] = current_csv
            #st.write(weathers)
            #st.write(results)
            scores = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
            top_recommendation = next(iter(scores))
            create_map(points[0][0], points[0][1], points)
            typewriter(f"Top recommented destination is : {top_recommendation}", 10)
            for (index, x) in enumerate(scores):
                st.markdown(
                    f"""
                    - {index + 1}'st Recommendation is: {x} | [Link]({url[x]})
                    """
                    )
            st.session_state.recommented_url = url[top_recommendation]
            st.session_state.best_csv = best_csv[top_recommendation]
            st.success('Done')
        
if __name__ == "__main__":
    st.sidebar.header("Menu")
    st.sidebar.write("")
    if st.sidebar.button('Show results'):
        st.session_state.screen = "result"
    
    if st.sidebar.button('Team'):
        st.session_state.screen = "welcome_screen"
    if st.sidebar.button('User input'):
        st.session_state.screen = "user_input"
        
    #if st.sidebar.button('How it works?'):
    #    st.session_state.screen = "how_it_works" 
        
    best_recommended_csv = None
    if st.session_state.screen == "welcome_screen":
        show_team()
    if st.session_state.screen == "result":
        show_results()
    if st.session_state.screen == "user_input":
        best_recommended_csv = user_input()
        # histogram_plot(best_recommended_csv)
    #if st.session_state.screen == "how_it_works":
    #    how_it_works()
    if(st.session_state.best_csv.empty):
        pass
    else:
        histogram_plot(st.session_state.best_csv)
    #data = pd.read_csv("../api/data.csv")
    #fig = plot_weather_data(data, )
    #print(st.session_state.screen)
