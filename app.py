import streamlit as st
import pandas as pd
import numpy as np
import requests
from numpy.random import randint
import plotly.express as px

st.markdown('''# Simple Interface for ectricity-consumption-decipherer ''')

#upload file to api:
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  ipnut_df = pd.read_csv(uploaded_file)
  st.write(ipnut_df)


#load data from api:
#api_url = 'https://taxifare.lewagon.ai/predict'
#res = requests.get(api_url, params = df)
#st.write(res.text)
#data = res.json()


#function for graphs:
st.markdown("## Global Electricity Consumption")

def graph_pie(df):
    col_values = [val for val in df.sum()]
    col_names = [col for col in df.columns]

    data_agr_api = {'type': col_names,'consumption_%': col_values}
    data_agr_api_df = pd.DataFrame(data = data_agr_api)
    pie_chart = px.pie(data_agr_api_df,
                   values = "consumption_%",
                   names = "type")

    return st.plotly_chart(pie_chart)
def graph_line(df):
    chart_data = pd.DataFrame(
        df,
        columns = df.columns)

    return st.line_chart(chart_data)

#random data for test - rooms:
rooms = ['kitchen','laundry','others']
n_rows = 50
df = pd.DataFrame(
    np.random.randint(100, size=(n_rows, len(rooms))),
    columns = rooms)
df
#Visual:
st.subheader("Electricity breakdown by rooms ")
graph_pie(df)

st.subheader("Electricity consupmtion during the given period")
graph_line(df)

room = st.selectbox(
    'Choose the room to see details on equipments consumption',
    (rooms)
    )
st.write('You selected:', room)

#random data for test -equipments:
equipment_list_1 = ['refrigerator','oven', 'Coffee_Brewer', 'Toaster','Microwave'] #kitchen
equipment_list_2 = ['washer', 'dryer', 'equipment_3','equipment_4','equipment_5'] #laundry
equipment_list_3 = ['AC', 'water_heater', 'other_1','other_2'] #others
n_rows = 50
room1_eq_df = pd.DataFrame(
    np.random.randint(n_rows, size=(n_rows, len(equipment_list_1))),
    columns = equipment_list_1)
room2_eq_df = pd.DataFrame(
    np.random.randint(n_rows, size=(n_rows, len(equipment_list_2))),
    columns = equipment_list_2)
room3_eq_df = pd.DataFrame(
    np.random.randint(n_rows, size=(n_rows, len(equipment_list_3))),
    columns = equipment_list_3)


#Details:
agree = st.button("Click to see equpment breakdown in" + str(room))
if agree:
    if room == rooms[0]:
        graph_pie(room1_eq_df)
        graph_line(room1_eq_df)
    elif room == rooms[1]:
        graph_pie(room2_eq_df)
        graph_line(room2_eq_df)
    elif room == rooms[2]:
        graph_pie(room3_eq_df)
        graph_line(room3_eq_df)
