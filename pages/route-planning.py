import streamlit as st
from backend.data_source import *
from backend.utils import string_to_array
from backend.map_application import *
from backend.logistic import *
import pandas as pd
from streamlit_folium import folium_static

# side bar page view
with st.sidebar:
    #api_token = st.text_input('API Token', type='password')
    api_token = st.secrets['open_route_service']
    
    st.caption('Enter Geocoordinates of the Depot')
    depot_location_x = st.text_input('Depot Location X', value='4.85')
    depot_location_y = st.text_input('Depot Location Y', value='100.74')
    vehicles_number = st.number_input('Number of Vehicles', min_value=1, max_value=10, value=3)
    
    depot_geocoordinates = string_to_array(depot_location_x, depot_location_y)
    enable_map = st.button('Create Visualization', type='primary')
    enable_optimization = st.button('Optimize Route', type='secondary')


# main page view
st.title('Route Planning Engine')

st.caption('If you use predefined data, the file upload step will be hidden.')
predefined_data_on = st.toggle('Use Predefined Data', True)
data = get_data('sample_data.csv')

if predefined_data_on == False:
    with st.expander('Upload CSV Data File'):
        uploaded_file = st.file_uploader("Upload a CSV file")
        # display the uploaded file as a dataframe
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file, index_col='ID', parse_dates=['Open_From', 'Open_To'])

# map view
m = create_map(depot_geocoordinates)
m = add_depot_marker(m, depot_geocoordinates)
m = add_marker(m, data)

with st.expander('Locations Preview', expanded=True):
    if enable_map:
        folium_static(m)
    
# optimization view
if enable_optimization:
    vehicles = get_vehicles(vehicles_number, depot_geocoordinates)
    deliveries = get_delivery_stations(data)
    ors_client = get_ors_client(api_token)
    result = get_optimization(ors_client, vehicles, deliveries)
    m = add_optimized_route(m, result)

with st.expander('Optimized Route Preview', expanded=True):
    if enable_optimization:
        folium_static(m)

# report analysis
if enable_optimization:
    report_table = generate_report_table(result)

with st.expander('Optimization Report', expanded=True):
    if enable_optimization:
        st.write(report_table)
    
if enable_optimization:
    schedule_table = generate_schedule_table(result)

with st.expander('Optimization Schedule', expanded=True):
    if enable_optimization:
        for i in range(len(schedule_table)):
            st.write(f'Vehicle {i+1}')
            df = iterative_schedule(schedule_table, i, data)
            st.write(df)