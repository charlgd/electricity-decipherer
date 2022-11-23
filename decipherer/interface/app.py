import streamlit as st
import pandas as pd
import numpy as np
import requests
from numpy.random import randint
import plotly.express as px

st.markdown('''# Simple Interface for ectricity-consumption-decipherer ''')

def input_interface():
    '''the function generates a checkbox so that the user can select their room type
      and if he has a Bedroom, then it creates a slider - to select the number of bedrooms
    '''
    user_data = ['Kitchen', 'Laundry room', 'Bedroom', 'Bathroom']
    st.header('Choose the type of rooms in your house')
    user_selected_data =[]

    for i in range(len(user_data)):
        ch = st.checkbox(user_data[i])
        user_selected_data.append(ch)

    # if user has 'Bedroom room' then ask number of bedrooms (from 1 to 10)
    if user_selected_data[2]:
        bedroom_count = st.slider('Select a number of bedrooms', 1, 10, 1)

    #create list of selected rooms:
    rooms = [user_data[np.where(user_selected_data)[0][i]] \
        for i in range(len(np.where(user_selected_data)[0]))]

    return rooms


#upload file to api:
uploaded_file = st.file_uploader("Choose a file (in csv format)")
analyze_btn = None
if uploaded_file is not None:
    ext = uploaded_file.name.split(".")[-1]
    if ext == 'csv':
        ipnut_df = pd.read_csv(uploaded_file)
        st.markdown('Number of rows  = '+ str(ipnut_df.shape[0]))
        st.table(data = ipnut_df[:5])
        #ask user for type of rooms and number of bedrooms:
        rooms = input_interface()
        analyze_btn = st.button("Click to analyze my electricity consumption" )
    else:
        st.markdown("## Please upload file in csv format ")


#function for graphs:
def graph_pie(df):
    '''Input Dataframe,
    the function aggregates the data and returns a pie chart
    '''
    col_values = [val for val in df.sum()]
    col_names = [col for col in df.columns]

    data_agr_api = {'type': col_names,'consumption_%': col_values}
    data_agr_api_df = pd.DataFrame(data = data_agr_api)

    pie_chart = px.pie(data_agr_api_df,
                   values = "consumption_%",
                   names = "type")

    return st.plotly_chart(pie_chart, use_container_width=True)

def graph_line(df):
    '''Input Dataframe,
    the function returns a line graph
    '''
    chart_data = pd.DataFrame(
        df,
        columns = df.columns)

    return st.line_chart(chart_data)


if analyze_btn:
    #random data for test - rooms:
    n_rows = 50
    df = pd.DataFrame(
        np.random.randint(100, size=(n_rows, len(rooms))),
        columns = rooms)

    #Visual:
    st.subheader("Electricity breakdown by rooms ")
    graph_pie(df)

    st.subheader("Electricity consupmtion during the given period")
    graph_line(df)
