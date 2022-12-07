from numpy.random import randint
import streamlit as st
import pandas as pd
import numpy as np
import requests
from numpy.random import randint
import plotly.express as px
import json
import os


#Interface for Rooms:
def input_interface():
    '''the function generates a checkbox so that the user can select their room type
      and if he has a Bedroom, then it creates a slider - to select the number of bedrooms
      return list of room type and the number of bedrooms
    '''
    user_data = ['Bathroom', 'Bedroom', 'Heating room', 'Kitchen', 'Laundry room']
    user_data_default = []
    user_selected_data =[]

    for i in range(len(user_data)):
        if user_data[i] in user_data_default:
            ch = st.checkbox(label = user_data[i], value =True)
        else:
            ch = st.checkbox(user_data[i])
        user_selected_data.append(ch)
        if i == 1:
            bedroom_count = st.slider('Choose the number of bedrooms', 1, 10, 0)

    #create list of selected rooms:
    rooms = [user_data[np.where(user_selected_data)[0][i]] \
        for i in range(len(np.where(user_selected_data)[0]))]

    return rooms, bedroom_count

def df_to_api(df_input, url):
    '''convert dataframe (df) to json file
    and post it (url), return response
    '''
    json_list = json.loads(json.dumps(list(df_input.T.to_dict().values())))
    res = requests.post(url, data = json.dumps(json_list))
    return res

def api_to_df(res):
    '''get response  (res) from df_to_api(df, url)
    and convert data to dataframe (df),
    return dataframe
    '''
    dict_url = res.json()
    df_output = pd.DataFrame(dict_url)
    return df_output

def check_csv_headers(df):
    '''
    get dataframe and check the columns,
    return True / False
    '''
    uploaded_file_headers = ['date','time','global_active_power',\
            'global_reactive_power','voltage',\
            'global_intensity','global_consumption']
    return list(df.columns) == uploaded_file_headers

def data_similation_rooms(df_csv):
    '''Create dataframe from uploaded csv:
    data from global consuption divided into 3 columns (rooms)
    '''
    n = df_csv.shape[1]
    heat_coef = np.random.uniform(0.65, 0.90, n)
    laun_coef = np.random.uniform(0.01, 0.10, n)

    total = [df_csv['global_consumption'].iloc[i] for i in range(n)]
    heating_room = [round(total[i] * heat_coef[i]) for i in range(n)]
    laundry_room  = [round(total[i] * laun_coef[i]) for i in range(n)]
    kitchen = [round(total[i] - heating_room[i]-laundry_room[i]) for i in range(n)]
    date_time = [df_csv['date'].iloc[i]+' '+ df_csv['time'].iloc[i] for i in range(n)]
    data_simil = {
        'kitchen': kitchen,
        'laundry_room': laundry_room,
        'heating_room': heating_room,
        'date_time': date_time
        }
    df_simil = pd.DataFrame(data_simil)
    return df_simil

def data_similation_appl(df_global_cons, appl_list):
    '''Create dataframe from global consuption in the room
    '''
    n = df_global_cons.shape[0]
    lst =[]
    for i in range(len(appl_list)):
        name = np.random.uniform(0.00, 3.18, n)
        lst.append(appl_list[i])
        lst.append(name)

    date_time = [df_global_cons['date_time'].iloc[i] for i in range(n)]

    it = iter(lst)
    res_dct = dict(zip(it, it))
    df44 = pd.DataFrame(res_dct)
    df_output = pd.concat([df_global_cons['date_time'], df44], axis=1)
    return df_output



def from_csv_for_api_appl(df_csv, room_type):
    '''modify df for api format:
    '''
    room_type = room_type.lower()
    if room_type in df_csv.columns or room_type == 'all':
        n = df_csv.shape[0]
        column_datetime = 'date_time'
        date_time = [df_csv[column_datetime].iloc[i] for i in range(n)]
        if room_type == 'all':
            #take the total sum in all columns except column with date info:
            consumption = [round(df_csv.loc[:, df_csv.columns != column_datetime].iloc[i].sum(),2) for i in range(n)]
        else:
            #take the data only in one coliumn = room_type:
            consumption = [df_csv[room_type].iloc[i] for i in range(n)]
        data_output = {
            'date_time': date_time,
            'consumption':consumption
            }
        df_output = pd.DataFrame(data_output)
    else:
        df_output = pd.DataFrame({'date_time': [''], 'room_type': [room_type]})
    return df_output

#Interface for Appliances:
def input_interface_appliances():
    '''the interface for appliences,
    return a list with selected appliences and selected room type
    1) kitchen -  dishwasher, an oven and a microwave (hot plates are not electric but gas powered).
    2) laundry_room - a washing-machine, a tumble-drier, a refrigerator and a light.
    3) heating_room - electric water-heater and an air-conditioner.
    '''
    user_data_appl = {
                   'Kitchen':['dishwasher','microwave','oven','coffee','freezer'\
                       ,'phone_charger','laptop','tv'],
                   'Laundry room':['washing_machine','tumble_drier','light','sound_system','internet_router', 'refrigerator'],
                   'Heating room':['water_heater','ac','boiler','radiator','fan']
                  }
    #Data by default selected:
    #appl_by_default_kitchen = ['Dishwasher','Oven','Microwave']
    #appl_by_default_laundry = ['Washing-machine','Dryer','Refrigerator','Light system']
    #appl_by_default_heating = ['Water-heater','Air-conditioner']

    # Title for this section
    #st.subheader("")

    #ask user to select room:
    room_type_list = list(user_data_appl.keys()) + ['All']
    room_type_list.sort()
    st.subheader('Select the room to analyze your energy consumption by appliance.')
    option = st.selectbox(
        '',
        (room_type_list),
        index = 1
        )
    #st.write('You selected:', option)
    room_type = option

    user_selected_data =[]
    user_data_appl_list= []
    col1, col2  = st.columns((0.5,1))
    with col1:
        #display data corresponding to user choice
        for i, (key, value) in enumerate(user_data_appl.items()):
            #1.If user select ALL rooms:
            if option == 'All':
                st.markdown("##### " + str(key.capitalize()))
                #create a list with all possible appliances -user_data_appl_list:
                appl_keys = [user_data_appl[i] for i in user_data_appl.keys()]
                for i in range(len(appl_keys)):
                    for j in range(len(appl_keys[i])):
                        user_data_appl_list.append(appl_keys[i][j])
                #create a list with selected appliances:
                for i in range(len(value)):
                    user_selected_data.append(st.checkbox(value[i].replace('_',' ').capitalize()))
                    #user_data_appl_list.append(value[i])

            #2.if user select one room:
            if key == option:
             st.markdown("##### " + str(key.capitalize()))
             #create a list with all possible appliances -user_data_appl_list:
             user_data_appl_list = user_data_appl[option]
             #create a list with selected appliances:
             for i in range(len(value)):
                #if value[i] in appl_by_default:
                    #ch = st.checkbox(value[i], key = str(value[i]), value  = True)
                ch = st.checkbox(value[i].replace('_',' ').capitalize())
                user_selected_data.append(ch)

    appl = [user_data_appl_list[np.where(user_selected_data)[0][i]] \
        for i in range(len(np.where(user_selected_data)[0]))]

    return appl,room_type


#Function for graphs:
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

def graph_pie(df, column_datetime):
    '''Input Dataframe,
    the function aggregates the data and returns a pie chart
    '''
    #do not take the last volumn with datetime
    #df = df.iloc[:,:-1]
    df = df.loc[:, df.columns != column_datetime]

    #watt-hour in col_values
    col_values = [val * ELEC_PRICE  for val in df.sum()]
    col_names = [col.capitalize().replace('_', ' ') for col in df.columns]

    data_agr_api = {'room': col_names,'CAD': col_values}
    data_agr_api_df = pd.DataFrame(data = data_agr_api)


    #display number of data  = number of columns in received dataset
    room_num = len(col_values)
    columns_num = ['col' + str(i) for i in range(room_num)]
    columns_num = st.columns(room_num)
    for i in range(room_num):
        columns_num[i].metric(col_names[i].replace('_room',' '), round(col_values[i],2), "CAD")

    pie_chart = px.pie(data_agr_api_df,
                   values = "CAD",
                   names = "room"
                   )

    return st.plotly_chart(pie_chart, use_container_width=True)

def graph_bar(df, col_dt_name):
    '''Input Dataframe, col_dt_name - name of column with datetime
    the function returns a bar chart
    '''
    chart_data = df
    chart_data.columns = [c.capitalize().replace('_', ' ') for c in df.columns]
    return st.bar_chart(chart_data, x = chart_data.columns[0])

def graph_line(df, col_dt_name):
    '''Input Dataframe, col_dt_name - name of column with datetime
    the function returns a line chart
    '''
    #col_dt_name = df.columns[-1]
    chart_data = pd.DataFrame(df, columns = df.columns)
    return st.line_chart(chart_data, x = col_dt_name)

#------Pages--------------------#

def RoomData():
    '''
    Page for rooms
    '''
    #upload csv file to api:
    st.markdown(
    """
    <style>
        .css-9ycgxx::after {
            content: " provided by your utility ⚡";
        }
    <style>
    """, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type = "csv")
    analyze_btn = None
    min_dt = ''
    max_dt = ''
    resp_code = 100
    df_from_api = pd.DataFrame()
    input_df = pd.DataFrame()
    df_output = pd.DataFrame()

    if uploaded_file is not None:
        file_name = uploaded_file.name
        input_df = pd.read_csv(uploaded_file)
        if len(input_df) > 1:
            if check_csv_headers(input_df):
                try:
                    df_1col = input_df.iloc[:, 0]

                    if input_df.columns[0] in ['Date','date','time', 'date_time', 'datetime']:
                            min_dt = str(df_1col.iloc[0])
                            max_dt = str(df_1col.iloc[-1])

                    st.success('The file was successfully uploaded!\
                            It contains the consumption profile of \
                            your home from ' + min_dt +' to '+ max_dt + '.', icon="✅")
                    #ask user for type of rooms and number of bedrooms:
                    rooms, bedroom_count = input_interface()
                    btn_check = 0
                    analyze_btn = st.button("Analyse my consumption ✨")
                    if analyze_btn:
                        st.session_state = 1
                        room_api_list = ['kitchen','laundry_room','bathroom','heating_room','bedroom']
                        url_rooms= '?'
                        for i in range(len(room_api_list)):
                            room_api = room_api_list[i]
                            room_url_part = str(room_api) + '=' + \
                                str(not not[bool(r) for r in rooms if r.replace(' ','_').lower() == room_api])
                            if room_api == 'bedroom':
                                room_url_part = str(room_api) +'=' + str(bedroom_count)
                            url_rooms = url_rooms + room_url_part + '&'
                        url_rooms = API_URL + url_rooms[:-1]

                        #st.write(url_rooms)

                        api_response = df_to_api(input_df, url_rooms)
                        resp_code = api_response.status_code

                        #st.write(resp_code)

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

        if st.session_state:
            #load data from api:
            try:
                if resp_code == 200:
                    #get data from api:
                    df_from_api = api_to_df(api_response)
                if resp_code != 200:
                    #Simulate data:
                    df_from_api = data_similation_rooms(input_df)
                #column name with datetime
                col_dt_name = 'date_time'

                df_from_api[col_dt_name] = pd.to_datetime(df_from_api[col_dt_name])
                df_output = df_from_api.copy()


                grouped_hours = df_from_api.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='H')).sum().reset_index()
                grouped_days = df_from_api.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='D')).sum().reset_index()

                grouped_Ch = grouped_hours.copy()
                grouped_Ch = grouped_Ch.groupby(grouped_Ch[col_dt_name].dt.hour).mean().reset_index()

                ###Visual:
                #convert W to kW:
                df_from_api.loc[:, df_from_api.columns != col_dt_name]\
                    = df_from_api.loc[:, df_from_api.columns != col_dt_name]/1000

                #total electricity consuption:
                el_consupt = round(sum(df_from_api.iloc[:,:-1].sum()),0)

                st.subheader("Electricity cost distribution by room (CAD)")
                st.markdown('The global electricity consumption of your home between ' \
                    + min_dt + ' and ' + max_dt + ' was ' + str(el_consupt) +
                    ' kWh. Here is how it is distributed among the different rooms:')

                graph_pie(df_from_api,col_dt_name)

                st.subheader("Evolution of your daily electricity consumption during the given period (kWh)")
                #graph_bar(df_from_api,col_dt_name)
                graph_bar(grouped_days,col_dt_name)

                st.subheader("Your electricity consumption by hours during a typical day (kWh)")
                graph_bar(grouped_Ch,col_dt_name)

            except requests.exceptions.RequestException as e:
                raise SystemExit(e)

    return df_output



def AppliancesData(df):
    '''
    Page for Appliances
    df = dataframe from the first page
    input_df = data from uploaded csv file
    '''
    #####Appliances:
    #1. user interface:
    appliances_list, room_type = input_interface_appliances()

    #1. send json (datetime, global_consuption, room_type)
    if len(appliances_list) > 0:
        analyze_btn_2 = st.button("Analyse my appliances ✨", key = 'btn_appl')

        appliances_list = list(dict.fromkeys(appliances_list))
        appliances_string = ','.join(str(i) for i in appliances_list) #.split(":", 1)
        room_type = room_type.replace(' ','_')
        url_appl = API_URL + '/appliances?type=' + room_type.lower() + '&appliance_list='\
        + appliances_string
        #st.write('data to api:')
        #st.write(url_appl)

        if analyze_btn_2:
            #st.write("Data to API from the first api")
            #st.write(df)
            df_api_cons = from_csv_for_api_appl(df, room_type)
            #st.write(df_api_cons)

            if len(df_api_cons) > 1:
                col_dt_name = 'date_time'
                df_api_cons[col_dt_name] = df_api_cons[col_dt_name].dt.strftime('%Y-%m-%d %H:%M:%S')

                resp_ap = df_to_api(df_api_cons,url_appl)
                #st.write("data to api:")
                #st.write(df_api_cons)

                df_appl_det = api_to_df(resp_ap)
                df_appl_det[col_dt_name] = pd.to_datetime(df_appl_det[col_dt_name])
                #st.write("data from api - appl:")
                #st.write(df_appl_det)

                #st.markdown('#### Here is how it is distributed among the different appliances that you selected:')
                #st.write(resp_ap.status_code)
                #st.write(df_appl_det)
                if resp_ap.status_code != 200:
                    #df_api_cons = from_csv_for_api_appl(df, room_type)
                    df_appl_det = data_similation_appl(df,appliances_list)
                    st.write("Simulated data:")
                    #st.write(df_appl_det)
                    #########

                #df_appl_deteail[col_dt_name] = pd.to_datetime(df_appl_deteail[col_dt_name])
                if col_dt_name in df_appl_det.columns:
                    grouped_hours = df_appl_det.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='H')).sum().reset_index()
                    grouped_days = df_appl_det.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='D')).sum().reset_index()
                ###Visual:
                #convert Wt to Kwt:
                    df_appl_det.loc[:, df_appl_det.columns != col_dt_name]\
                    = df_appl_det.loc[:, df_appl_det.columns != col_dt_name]
                            #/1000

                    #total electricity consuption:
                    st.subheader("Electricity cost breakdown by appliance (CAD)")
                    if room_type == 'All':
                        room_string = 'all your rooms'
                    else:
                        room_string = 'your ' + room_type.lower().replace('_',' ')
                    st.markdown('Here is how it is distributed among the different appliances in '+ room_string + ':')
                    graph_pie(df_appl_det, col_dt_name)
            else:
                st.write("No data in this room")
    else:
        st.markdown('##### Please select appliances.')



############################################
API_URL = os.environ.get("API_URL")
ELEC_PRICE = 0.103
col_dt_name = 'date_time'

st.set_page_config(
    page_title="HomeAIVolt", page_icon="⚡", initial_sidebar_state="expanded"
)

st.markdown('''# ⚡ HomeAIVoltX''')
st.markdown('''## Get smart about your energy usage.''')
st.markdown('''## Unlock the power of data to reduce energy costs.''')
st.markdown('''## Take control of your energy bills with HomeAIVolt.''')

#df_from_api = pd.DataFrame()
#df_from_api = RoomData()

# -------------- ROOM DATA
#upload csv file to api:
st.markdown(
"""
<style>
    .css-9ycgxx::after {
        content: " provided by your utility ⚡";
    }
<style>
""", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type = "csv")
analyze_btn = None
min_dt = ''
max_dt = ''
resp_code = 100
df_from_api = pd.DataFrame()
input_df = pd.DataFrame()
df_output = pd.DataFrame()

if uploaded_file is not None:
    file_name = uploaded_file.name
    input_df = pd.read_csv(uploaded_file)
    if len(input_df) > 1:
        if check_csv_headers(input_df):
            try:
                df_1col = input_df.iloc[:, 0]

                if input_df.columns[0] in ['Date','date','time', 'date_time', 'datetime']:
                        min_dt = str(df_1col.iloc[0])
                        max_dt = str(df_1col.iloc[-1])

                st.success('The file was successfully uploaded!\
                        It contains the consumption profile of \
                        your home from ' + min_dt +' to '+ max_dt + '.', icon="✅")
                #ask user for type of rooms and number of bedrooms:
                rooms, bedroom_count = input_interface()
                btn_check = 0
                analyze_btn = st.button("Analyse my consumption ✨")
                if analyze_btn:
                    st.session_state = 1
                    room_api_list = ['kitchen','laundry_room','bathroom','heating_room','bedroom']
                    url_rooms= '?'
                    for i in range(len(room_api_list)):
                        room_api = room_api_list[i]
                        room_url_part = str(room_api) + '=' + \
                            str(not not[bool(r) for r in rooms if r.replace(' ','_').lower() == room_api])
                        if room_api == 'bedroom':
                            room_url_part = str(room_api) +'=' + str(bedroom_count)
                        url_rooms = url_rooms + room_url_part + '&'
                    url_rooms = API_URL + url_rooms[:-1]

                    #st.write(url_rooms)

                    api_response = df_to_api(input_df, url_rooms)
                    resp_code = api_response.status_code

                    #st.write(resp_code)

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

    if st.session_state:
        #load data from api:
        try:
            #if resp_code == 200:
                #get data from api:
            df_from_api = api_to_df(api_response)
            #if resp_code != 200:
                #Simulate data:
                #df_from_api = data_similation_rooms(input_df)
            #column name with datetime
            col_dt_name = 'date_time'

            df_from_api[col_dt_name] = pd.to_datetime(df_from_api[col_dt_name])
            df_output = df_from_api.copy()


            grouped_hours = df_from_api.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='H')).sum().reset_index()
            grouped_days = df_from_api.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='D')).sum().reset_index()

            grouped_Ch = grouped_hours.copy()
            grouped_Ch = grouped_Ch.groupby(grouped_Ch[col_dt_name].dt.hour).mean().reset_index()

            ###Visual:
            #convert W to kW:
            df_from_api.loc[:, df_from_api.columns != col_dt_name]\
                = df_from_api.loc[:, df_from_api.columns != col_dt_name]/1000

            #total electricity consuption:
            el_consupt = round(sum(df_from_api.iloc[:,:-1].sum()),0)

            st.subheader("Electricity cost distribution by room (CAD)")
            st.markdown('The global electricity consumption of your home between ' \
                + min_dt + ' and ' + max_dt + ' was ' + str(el_consupt) +
                ' kWh. Here is how it is distributed among the different rooms:')

            graph_pie(df_from_api,col_dt_name)

            st.subheader("Evolution of your daily electricity consumption during the given period (kWh)")
            #graph_bar(df_from_api,col_dt_name)
            graph_bar(grouped_days,col_dt_name)
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            st.subheader("Your electricity consumption by hours during a typical Day (kWh)")
            graph_bar(grouped_Ch,col_dt_name)

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

# -------------- APPLIANCE DATA

if len(df_from_api) > 1:
    #AppliancesData(df_from_api)
    #graph_bar(data, col_dt_name = data.columns[-1])

        #####Appliances:
    #1. user interface:
    appliances_list, room_type = input_interface_appliances()

    #1. send json (datetime, global_consuption, room_type)
    if len(appliances_list) > 0:
        analyze_btn_2 = st.button("Analyse my appliances ✨", key = 'btn_appl')

        appliances_list = list(dict.fromkeys(appliances_list))
        appliances_string = ','.join(str(i) for i in appliances_list) #.split(":", 1)
        room_type = room_type.replace(' ','_')
        url_appl = API_URL + '/appliances?type=' + room_type.lower() + '&appliance_list='\
        + appliances_string
        #st.write('data to api:')
        #st.write(url_appl)

        if analyze_btn_2:
            #st.write("Data to API from the first api")
            #st.write(df)
            df_api_cons = from_csv_for_api_appl(df_output, room_type)
            #st.write(df_api_cons)

            if len(df_api_cons) > 1:
                col_dt_name = 'date_time'
                df_api_cons[col_dt_name] = df_api_cons[col_dt_name].dt.strftime('%Y-%m-%d %H:%M:%S')

                resp_ap = df_to_api(df_api_cons,url_appl)
                #st.write("data to api:")
                #st.write(df_api_cons)

                df_appl_det = api_to_df(resp_ap)
                df_appl_det[col_dt_name] = pd.to_datetime(df_appl_det[col_dt_name])
                #st.write("data from api - appl:")
                #st.write(df_appl_det)

                #st.markdown('#### Here is how it is distributed among the different appliances that you selected:')
                #st.write(resp_ap.status_code)
                #st.write(df_appl_det)
                #if resp_ap.status_code != 200:
                    #df_api_cons = from_csv_for_api_appl(df, room_type)
                    #df_appl_det = data_similation_appl(df,appliances_list)
                    #st.write("Simulated data:")
                    #st.write(df_appl_det)
                    #########

                #df_appl_deteail[col_dt_name] = pd.to_datetime(df_appl_deteail[col_dt_name])
                if col_dt_name in df_appl_det.columns:
                    grouped_hours = df_appl_det.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='H')).sum().reset_index()
                    grouped_days = df_appl_det.groupby(pd.Grouper(key=col_dt_name, axis=0, freq='D')).sum().reset_index()
                ###Visual:
                #convert Wt to Kwt:
                    df_appl_det.loc[:, df_appl_det.columns != col_dt_name]\
                    = df_appl_det.loc[:, df_appl_det.columns != col_dt_name]
                            #/1000

                    #total electricity consuption:
                    st.subheader("Electricity cost breakdown by appliance (CAD)")
                    if room_type == 'All':
                        room_string = 'all your rooms'
                    else:
                        room_string = 'your ' + room_type.lower().replace('_',' ')
                    st.markdown('Here is how it is distributed among the different appliances in '+ room_string + ':')

                    appl_list = ['Dishwasher', 'Microwave', 'Oven']
                    graph_pie(df_appl_det, col_dt_name)
            else:
                st.write("No data in this room")
    else:
        st.markdown('##### Please select appliances.')



#################
