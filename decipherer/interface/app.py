import streamlit as st
import pandas as pd
import numpy as np
import requests
from numpy.random import randint
import plotly.express as px
import json


st.markdown('''# OhmAIVolt''')
st.markdown('''## Ectricity consumption decipherer ''')
st.markdown('''''')
def input_interface():
    '''the function generates a checkbox so that the user can select their room type
      and if he has a Bedroom, then it creates a slider - to select the number of bedrooms
    '''
    user_data = ['Kitchen', 'Bedroom', 'Laundry room', 'Bathroom','Heating room']
    user_selected_data =[]


    for i in range(len(user_data)):
        ch = st.checkbox(user_data[i])
        user_selected_data.append(ch)
         # if user has 'Bedroom room' then ask number of bedrooms (from 1 to 10)
        if i == 1: #user_selected_data[1]:
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
    '''get response from df_to_api(df, url)
    and convert data to dataframe (df),
    return dataframe
    '''
    #res = requests.get(url)
    dict_url = res.json()
    #df = pd.DataFrame(dict_url.get("data"))
    df = pd.DataFrame(dict_url)
    return df

def check_csv_headers(df):
    '''
    get dataframe and check the columns,
    return True / False
    '''
    #date,time,global_active_power,global_reactive_power,voltage,global_intensity,global_consumption

    uploaded_file_headers = ['date','time','global_active_power',\
            'global_reactive_power','voltage',\
            'global_intensity','global_consumption'] #set as a global variable
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
    df = df.loc[:, df.columns != 'datetime']

    col_values = [val for val in df.sum()]
    col_names = [col for col in df.columns]
    data_agr_api = {'type': col_names,'consumption_%': col_values}
    data_agr_api_df = pd.DataFrame(data = data_agr_api)
    pie_chart = px.pie(data_agr_api_df,
                   values = "consumption_%",
                   names = "type")
    return st.plotly_chart(pie_chart, use_container_width=True)

def graph_bar(df):
    '''Input Dataframe,
    the function returns a bar chart
    '''
    chart_data = pd.DataFrame(df,columns = df.columns)
    return st.bar_chart(chart_data, x = 'datetime')

#function for graphs - test:
def graph_bar_test(df):
    '''Input Dataframe,
    the function returns a line graph
    '''
    chart_data = pd.DataFrame(df,columns = df.columns)

    return st.bar_chart(chart_data)

#upload csv file to api:
uploaded_file = st.file_uploader("", type = "csv")
analyze_btn = None



if uploaded_file is not None:
    file_name = uploaded_file.name
    ipnut_df = pd.read_csv(uploaded_file)
    if check_csv_headers(ipnut_df):
        #st.markdown("## File is uploading .......")
        with st.spinner('Wait for it...'):
            #csv to api:
            url =  'https://decipherer.loca.lt' #set as a global variable
        try:
            api_response = df_to_api(ipnut_df ,url)
            st.write(api_response)
            st.success('File was uploaded successfully!', icon="✅")
        except requests.exceptions.RequestException as err:
            st.write ("OOps: Something Else",err)
        except requests.exceptions.HTTPError as errh:
            st.write ("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            st.write ("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            st.write ("Timeout Error:",errt)
    else:
        st.warning("## File has a worng Headers!")


    #display number of rows:
    st.markdown('Number of rows  = '+ str(ipnut_df.shape[0]))
    #display min and max date:
    df_1col = ipnut_df.iloc[:, 0]
    if ipnut_df.columns[0] in ['Date','date','time', 'date_time', 'key']:
        st.markdown('Min date:'+ str(df_1col.min()))
        st.markdown('Max date:'+ str(df_1col.max()))
    #ask user for type of rooms and number of bedrooms:
    rooms = input_interface()
    analyze_btn = st.button("Analyse my consumption" )

if analyze_btn:
    #load data from api:
    try:
        if api_response.status_code == 200:
            df_from_api = api_to_df(api_response)
            #Visual:
            st.subheader("Electricity breakdown by rooms ")
            graph_pie(df_from_api)
            st.subheader("Electricity consumption during the given period")
            graph_bar(df_from_api)

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)


    #TEST DATA
    #random data for test - rooms:
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
