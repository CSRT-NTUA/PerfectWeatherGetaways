import streamlit as st
from streamlit_folium import folium_static
import folium

def create_map(lat, lon):
    # Set up Streamlit app title
    st.title("Customized Folium Map in Streamlit")

    # Create a Folium map object with custom attributes
    m = folium.Map(location=[lat, lon], zoom_start=10, control_scale=True)

    # Add a marker with a custom icon and popup
    folium.Marker(location=[lat, lon], popup='Destination', icon=folium.Icon(icon='cloud')).add_to(m)

    # Add a heatmap layer to the map
    #heat_data = [(51.5, -0.1, 1), (51.55, -0.2, 2), (51.6, -0.15, 3)]
    #folium.plugins.HeatMap(heat_data).add_to(m)

    # Add layer control to switch between different map layers
    folium.LayerControl().add_to(m)

    # Display the map in Streamlit
    folium_static(m)
