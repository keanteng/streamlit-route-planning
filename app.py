import streamlit as st
from backend.data_source import convert_df

st.set_page_config(layout="wide")


st.title('🚚 Route Planning')
st.markdown(
    '''
    A route planning app that helps you find the shortest path between multiple locations.
    Useful for delivery drivers, salespeople, and anyone who needs to visit multiple locations.
    
    To use the application, make sure you have a valid API token from OpenRouteService. Also, 
    you may choose to use the template CSV file provided below to upload your locations or you can
    use the provided CSV file to test the application.
    '''
)

template_data = convert_df('template.csv')
sample_data = convert_df('sample_data.csv')

st.caption('You can download the template CSV file below:')
st.download_button(
    label='Download Template CSV',
    data=template_data,
    file_name='template.csv',
    mime='text/csv'
)

st.caption('You can download the sample CSV file below:')
st.download_button(
    label='Download Sample CSV',
    data=sample_data,
    file_name='sample_data.csv',
    mime='text/csv'
)