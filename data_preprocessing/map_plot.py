import streamlit as st
from streamlit_folium import folium_static
import folium

def create_map(lat, lon, locations):
    # Set up Streamlit app title
    st.title("Destination mapping")

    # Create a Folium map object with custom attributes
    m = folium.Map(location=[lat, lon], zoom_start=10, control_scale=True)
    
    for loc in locations:
        folium.Marker(location=[loc[0], loc[1]], popup="Recommendation", icon=folium.Icon(icon='exclamation-sign')).add_to(m)
    # Add a marker with a custom icon and popup
    folium.Marker(location=[lat, lon], popup='Recommendation', icon=folium.Icon(icon='exclamation-sign')).add_to(m)
    folium.LayerControl().add_to(m)
    # Add a heatmap layer to the map
    #heat_data = [(51.5, -0.1, 1), (51.55, -0.2, 2), (51.6, -0.15, 3)]
    #folium.plugins.HeatMap(heat_data).add_to(m)

    # Add layer control to switch between different map layers
    folium.LayerControl().add_to(m)

    # Display the map in Streamlit
    folium_static(m)


if __name__ == "__main__":
    create_map(42.43242, 1.4124, [(41.2313, 1.421), (41.3231, '1.4141')])
