
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px
import json
import streamlit as st

url =  'https://decipherer.loca.lt/'
rooms = ['Kitchen', 'Bedroom', 'Laundry room', 'Bathroom']
n_rows = 50


col1, col2, col3 = st.columns(3)
col1.metric("Temperature", "70 °F", "1.2 °F")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

#st.write(df)
min_dt= '777'
max_dt = '22'
el_consupt = '333'

st.subheader("Electricity breakdown by rooms ")
st.markdown('#### The global electricity consumption of your home between' \
              + min_dt + 'and' + max_dt + ' was' + el_consupt +
            'Here is how it is distributed among the different rooms in your home:')

df = pd.DataFrame(
        np.random.randint(100, size=(n_rows, len(rooms))),
        columns = rooms)
df = df.loc[:, df.columns != 'Bathroom']
col_values = [val for val in df.sum()]
col_names = [col for col in df.columns]
data_agr_api = {'type': col_names,'consumption_%': col_values}
data_agr_api_df = pd.DataFrame(data = data_agr_api)
#print(df)
#print(data_agr_api_df)

#json_list = json.loads(json.dumps(list(ipnut_df.T.to_dict().values())))

#res = requests.post(url, data = json.dumps(json_list))
#print(res)

#def input_interface_appliances():
    #the interface for appliences



#df['DOB1'] = df['DOB'].dt.strftime('%m/%d/%Y')
#+ ' ' + x['time'])
#print(len(value))

#user_selected_data =[]
#print(type(user_data_appl))
#print(user_data_appl.items())
#print(user_data_appl.values())
#


#for key, value in user_data_appl.iteritems():
    #print(key)
##print(len(user_data_appl))
##for i in range(len(user_data_appl)):
   # ch = st.checkbox(user_data_appl[i])
   # user_selected_data.append(ch)
