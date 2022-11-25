from numpy.random import randint
import streamlit as st
import pandas as pd
import numpy as np
import requests
from numpy.random import randint
import plotly.express as px
import json
import os

API_URL = os.environ.get("API_URL")
ELEC_PRICE = 0.103

st.markdown('''# HomeAIVolt''')
st.markdown('''### HomeAIVolt uses powerful machine learning tools to analyse\
            the user’s electrical consumption data provided\
            by the utility company to suggest tailored recommendations\
            to the customer on reducing energy consumption and increasing their savings!\
            ''')
#st.markdown("<h1 style='text-align: center; color: red;'>Some title</h1>", unsafe_allow_html=True)
st.markdown('''#### Start by uploading the consumption\
    data of your apartment or house as a .csv file. \
        It is provided by your power utility company.
          ''')
st.markdown('''''')

def input_interface():
    '''the function generates a checkbox so that the user can select their room type
      and if he has a Bedroom, then it creates a slider - to select the number of bedrooms
    '''
    user_data = ['Kitchen', 'Bedroom', 'Laundry room', 'Bathroom','Heating room']
    user_data_default = ['Kitchen','Laundry room','Heating room']
    user_selected_data =[]

    for i in range(len(user_data)):
        if user_data[i] in user_data_default:
            ch = st.checkbox(label = user_data[i], value =True)
        else:
            ch = st.checkbox(user_data[i])
        user_selected_data.append(ch)
        if i == 1:
            bedroom_count = st.slider('Select a number of bedrooms', 1, 10, 0)

    #create list of selected rooms:
    rooms = [user_data[np.where(user_selected_data)[0][i]] \
        for i in range(len(np.where(user_selected_data)[0]))]

    return rooms

def df_to_api(df, url):
    '''convert dataframe (df) to json file
    and post it (url), return response
    '''
    json_list = json.loads(json.dumps(list(df.T.to_dict().values())))
    res = requests.post(url, data = json.dumps(json_list))
    return res

def api_to_df(res):
    '''get response  (res) from df_to_api(df, url)
    and convert data to dataframe (df),
    return dataframe
    '''
    dict_url = res.json()
    df = pd.DataFrame(dict_url)
    return df


def check_csv_headers(df):
    '''
    get dataframe and check the columns,
    return True / False
    '''
    uploaded_file_headers = ['date','time','global_active_power',\
            'global_reactive_power','voltage',\
            'global_intensity','global_consumption']
    return list(df.columns) == uploaded_file_headers


#function for graphs:
def graph_pie2(df):
    '''Input dataframe,
    the function aggregates the data and returns a pie chart
    '''
    df["kwh_data"] = pd.to_numeric(df["kwh_data"])
    df = df[['name','kwh_data']].groupby('name', as_index=False).agg({\
        'kwh_data':'sum'})
    data_agr_api = {'type': list(df["name"]),'consumption_%': list(df["kwh_data"])}
    data_agr_api_df = pd.DataFrame(data = data_agr_api)

    pie_chart = px.pie(data_agr_api_df,
                   values = "consumption_%",
                   names = "type")

    return st.plotly_chart(pie_chart, use_container_width=True)

def graph_pie(df):
    '''Input Dataframe,
    the function aggregates the data and returns a pie chart
    '''

    df = df.iloc[:,:-1]
    #watt-hour in col_values:
    col_values = [val/1000 * ELEC_PRICE  for val in df.sum()]

    col_names = [col.capitalize() for col in df.columns]

    data_agr_api = {'room': col_names,'watt-hour': col_values}

    data_agr_api_df = pd.DataFrame(data = data_agr_api)
    pie_chart = px.pie(data_agr_api_df,
                   values = "watt-hour",
                   names = "room")

    col1, col2, col3 = st.columns(3)
    col1.metric(col_names[0], round(col_values[0],2), "CAD")
    col2.metric(col_names[1], round(col_values[1],2), "CAD")
    col3.metric(col_names[2], round(col_values[2],2), "CAD")

    return st.plotly_chart(pie_chart, use_container_width=True)

def graph_bar(df, col_dt_name):
    '''Input Dataframe, col_dt_name - name of column with datetime
    the function returns a bar chart
    '''
    #col_dt_name = df.columns[-1]
    chart_data = pd.DataFrame(df,columns = df.columns)
    return st.bar_chart(chart_data, x = col_dt_name)

#function for graphs - test:
def graph_bar_test(df):
    '''Input Dataframe,
    the function returns a line graph
    '''
    chart_data = pd.DataFrame(df,columns = df.columns)

    return st.bar_chart(chart_data)


#--------------------------#
#upload csv file to api:
uploaded_file = st.file_uploader("", type = "csv")
analyze_btn = None
min_dt = ''
max_dt = ''

if uploaded_file is not None:
    file_name = uploaded_file.name
    ipnut_df = pd.read_csv(uploaded_file)
    if check_csv_headers(ipnut_df):
        try:
            api_response = df_to_api(ipnut_df, API_URL)

            df_1col = ipnut_df.iloc[:, 0]

            if ipnut_df.columns[0] in ['Date','date','time', 'date_time', 'datetime','key']:
                min_dt = str(df_1col.iloc[0])
                max_dt = str(df_1col.iloc[-1])

            st.success('The file was successfully uploaded!\
                    It contains the consumption profile of \
                    your home from ' + min_dt +' to '+ max_dt + '.', icon="✅")

        except requests.exceptions.RequestException as err:
            st.write ("OOps: Something Else",err)
        except requests.exceptions.HTTPError as errh:
            st.write ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            st.write ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            st.write ("Timeout Error:",errt)
    else:
        st.warning("## File has a wrong Headers!")


    #ask user for type of rooms and number of bedrooms:
    rooms = input_interface()
    analyze_btn = st.button("Analyse my consumption" )

if analyze_btn:
    #load data from api:
    try:
        if api_response.status_code == 200:
            df_from_api = api_to_df(api_response)
            df = df_from_api

            #column name with datetime
            col_dt_name = df_from_api.columns[-1]
            df_from_api[col_dt_name] = pd.to_datetime(df_from_api[col_dt_name])

            grouped_hours = df_from_api.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='H')).sum().reset_index()
            grouped_days = df_from_api.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='D')).sum().reset_index()

            #Visual:
            #total electricity consuption:
            el_consupt = round(sum(df.iloc[:,:-1].sum()),0)

            st.subheader("Electricity Cost (CAD) breakdown by rooms ")
            st.markdown('#### The global electricity consumption of your home between ' \
                + min_dt + ' and ' + max_dt + ' was ' + str(el_consupt) +
               ' kWh. ')
            st.markdown('#### Here is how it is distributed among the different rooms in your home:')
            graph_pie(df)

            st.subheader("Evolution of your electricity consumption (kWh) during the given period")
            graph_bar(df,col_dt_name)

            st.subheader("Electricity consumption by hours")
            graph_bar(grouped_hours,col_dt_name)

            st.subheader("Electricity consumption by days")
            graph_bar(grouped_days,col_dt_name)

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


    #TEST DATA
    #random data - in case api doesn't work:
    if api_response.status_code != 200:
        st.subheader("Random data")
        n_rows = 50
        df = pd.DataFrame(
            np.random.randint(100, size=(n_rows, len(rooms))),
            columns = rooms)
        #visual:
        st.subheader("Electricity breakdown by rooms ")
        graph_pie(df)
        st.subheader("Electricity consumption during the given period")
        graph_bar_test(df)
