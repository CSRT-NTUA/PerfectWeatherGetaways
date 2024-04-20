import streamlit as st
import plotly.express as px
import pandas as pd
import pydeck as pdk
import pycountry

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
    health_and_safety = ["Health & Safety"]
    others = ["Parking", "All-Inclusive Packages", "Rooms with Fireplace", "Rooms with Jacuzzi / Hot-Tub",
        "EV charging stations", "Gym", "Free Wi-Fi", "Business", "Accessible", "Sustainability Journey"]
    categories = [
        "Pool", "Spa", "Beachfront", "Dog Friendly", "Adult Only", "Honeymoon", "Skyscraper", 
        "Infinity Pool", "Luxury", "Historic", "Parking", "Boutique-Style", "Family", "Yoga", 
        "Ski In Ski Out", "Unusual", "Castle", "Cheap", "Overwater Bungalows", "Ski", "Vineyard", 
        "Monastery", "Small", "Romantic", "Nightlife", "5 Star", "4 Star", "3 Star", "Haunted", 
        "Pool Lap Lanes", "Pool Swim Up Bar", "Pool Water Slide", "Panoramic View Pool", "Rooftop Pool", 
        "Water Park", "Wave Pool", "Lazy River", "Private Pool", "Heated Pool", "Indoor Pool", "Outdoor Pool", 
        "Children's Pool", "Dogs Stay Free", "Dog Play Area", "Dog Sitting", "Rooms with Fireplace", 
        "All-Inclusive Packages", "Rooms with Jacuzzi / Hot-Tub", "Health & Safety", "EV charging stations", 
        "Gym", "Free Wi-Fi", "Business", "Treehouse", "Tennis", "Beach", "Accessible", "Casino", 
        "Sustainability Journey", "Golf"
    ]
    selected_categories = st.multiselect("Select Activities", categories)

"""def how_it_works():
    with open("api_test.py", 'r') as file:
        text = file.read()
    st.write("This is the api for asking info:")
    st.code(text, language='python')"""
    

def user_input():
    user_option = st.text_input("Enter: ")
    
    
    st.markdown("<h4 style='text-align: center;'>Add more options for your trip</h4>", unsafe_allow_html=True)

    st.markdown("#### Select dates")
    date_of_arrival = st.date_input('Date of arrival')
    date_of_deperature = st.date_input('Date of departure')
    
    st.markdown("#### Select Country")
    countries = [(country.name, country.alpha_2) for country in pycountry.countries]
    selected_country = st.selectbox("Select a country", countries, format_func=lambda x: x[0])
    flag_url = get_flag_url(selected_country[1])
    st.image(flag_url, width=32)
    
    st.markdown("#### Select Country")
    st.radio('Weather:', ['Sunny','Rainy'])
    
    st.markdown("#### Select Activities")
    show_categories()
    

    st.button('Search')
    
    
    

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