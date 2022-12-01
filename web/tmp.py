
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px
import json
import streamlit as st


st.set_page_config(
    page_title="HomeAIVolt", page_icon="⚡", initial_sidebar_state="expanded"
)


def input_interface():
    '''the function generates a checkbox so that the user can select their room type
      and if he has a Bedroom, then it creates a slider - to select the number of bedrooms
      return list of room type and the number of bedrooms
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

    return rooms, bedroom_count


#########Interface for Appliances:
def input_interface_appliances():
    '''the interface for appliences,
    return a list with selected appliences and selected room type
    1) kitchen -  dishwasher, an oven and a microwave (hot plates are not electric but gas powered).
    2) laundry_room - a washing-machine, a tumble-drier, a refrigerator and a light.
    3) heating_room - electric water-heater and an air-conditioner.
    '''
    user_data_appl = {
                   'kitchen':['Blender','Dishwasher','Oven','Toaster','Coffee machine','Microwave','Kettle'],
                   'laundry':['Washing-machine','Dryer','Refrigerator','Light system'],
                   'heating room':['Water-heater','Air-conditioner']
                  }

    appl_by_default_kitchen = ['Dishwasher','Oven','Microwave']
    appl_by_default_laundry = ['Washing-machine','Dryer','Refrigerator','Light system']
    appl_by_default_heating = ['Water-heater','Air-conditioner']

    #ask user to select room. By default - kitchen:
    room_type_list = list(user_data_appl.keys()) #+ ['All']
    option = st.selectbox(
        'Select the rooom - to see appliances in it',
        (room_type_list),
        index = 1,
        key = 'visibility'
        )
    st.write('You selected:', option)
    appl_by_default = []
    room_type = option
    #for kitchen
    if room_type == room_type_list[0]:
        appl_by_default = appl_by_default_kitchen
    #for laundry
    if room_type == room_type_list[1]:
        appl_by_default = appl_by_default_laundry
    #for heating room
    if room_type == room_type_list[2]:
        appl_by_default = appl_by_default_heating

    user_selected_data =[]
    user_data_appl_list= []
    col1, col2  = st.columns((0.5,1))
    user_data_appl[option]
    with col1:
        for i, (key, value) in enumerate(user_data_appl.items()):
            #display data corresponding to user choice
            if key == option:
             st.markdown("## " + str(key))
             for i in range(len(value)):
                 #######
                if value[i] in appl_by_default:
                    ch = st.checkbox(value[i], key = str(value[i]), value  = True)
                else:
                    ch = st.checkbox(value[i])
                user_selected_data.append(ch)
                 ######
                 #ch = st.checkbox(value[i], key = str(value[i]))
                 #if value[i] in appl_by_default:
                    #st.checkbox(label = value[i], value =True)

                user_data_appl_list.append(value[i])
                #user_selected_data.append(ch)

    #create list of selected appliences:
    appl = [user_data_appl_list[np.where(user_selected_data)[0][i]] \
        for i in range(len(np.where(user_selected_data)[0]))]

    #add default data:
    appl = appl + appl_by_default

    return appl,room_type

def graph_bar(df, col_dt_name):
    '''Input Dataframe, col_dt_name - name of column with datetime
    the function returns a bar chart
    '''
    chart_data = pd.DataFrame(df,columns = df.columns)
    return st.bar_chart(chart_data, x = col_dt_name)


def RoomData():
    df = pd.DataFrame({
                    'laundry': [18, 20, 15, 14, 10, 9],
                    'kitchen': [18, 20, 15, 14, 10, 9],
                    'time': ['2022-01-01 01:14:00', '2022-01-01 01:24:15',
                            '2022-01-01 02:52:19', '2022-01-01 02:52:00',
                            '2022-01-01 04:05:10', '2022-01-01 05:35:09']
        })#
    # Countries code goes here
    st.write("Page 1 - Countries")
    input_interface()
    return df

def ApplData():
    # Continents code goes here
    st.write("Page 2 !!!!!!")
    appl,room_type = input_interface_appliances()
    #st.write(appl)

###########################
st.header("⚡ HomeAIVolt")
df = RoomData()

btn_next = st.button("Go to the next page✨")
if st.session_state or btn_next:
    ApplData()
    graph_bar(df,'time')
