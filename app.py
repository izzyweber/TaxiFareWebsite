import datetime
import streamlit as st
import requests
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="IZZY TAXI",  # => Quick reference - Streamlit
    page_icon="🚕",
    layout="centered",  # wide
    initial_sidebar_state="auto")  # collapsed
'''
# 🚕 IZZY'S NYC TAXI FARE PREDICTOR 🚕
'''
col0, col1, col2 = st.columns(3)
passenger_count = col0.selectbox(
    'How many passengers?', (1, 2, 3, 4, 5, 6, 7, 8))
d = col1.date_input(
    "What day will you hail the cab?",
    datetime.date(2021, 8, 24))
#col1.write('Pickup date:', d)

t = col2.time_input('What time of day?', datetime.time(8, 45))
#col2.write('Cab will arrive at:', t)

col3, col4 = st.columns(2)
pickup_longitude = col3.text_input('Enter pickup longitude', 40.7614327)
#st.write('The current movie title is', title)

pickup_latitude = col4.text_input('Enter pickup latitude', -73.9798156)
#st.write('The current movie title is', title)

col5, col6 = st.columns(2)
dropoff_longitude = col5.text_input('Enter dropoff longitude', 40.6513111)
#st.write('The current movie title is', title)

dropoff_latitude = col6.text_input('Enter dropoff latitude', -73.8803331)
#st.write('The current movie title is', title)

pickup_datetime = str(d) + " " + str(t)

def convert_to_UTC(pickup_datetime):
    from datetime import datetime
    import pytz
    # create a datetime object from the user provided datetime
    pickup_datetime = datetime.strptime(pickup_datetime, "%Y-%m-%d %H:%M:%S")
    # localize the user datetime with NYC timezone
    eastern = pytz.timezone("US/Eastern")
    localized_pickup_datetime = eastern.localize(pickup_datetime, is_dst=None)
    utc_pickup_datetime = localized_pickup_datetime.astimezone(pytz.utc)
    return utc_pickup_datetime

pickup_datetime = convert_to_UTC(pickup_datetime).strftime("%Y-%m-%d %H:%M:%S")
params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

url = 'https://taxifare.lewagon.ai/predict'
json = requests.get(url, params).json()
dollar_fare = round(json["prediction"], 2)
st.write(f'## YOUR 100% ACCURATE FARE IS: ${dollar_fare}*')

data = pd.DataFrame([[float(pickup_longitude), float(pickup_latitude)], [
                    float(dropoff_longitude), float(dropoff_latitude)]], columns=['lat', 'lon'])
st.map(data)

st.write("**Please note we take no responsibility for the acutal accuracy of our predicted fares. This model is based on a dataset that is several years old.")
