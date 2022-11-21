import streamlit as st
import pandas as pd
import numpy as np
import requests
from numpy.random import randint

st.markdown('''# Simple Interface for electircity consumption''')


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
   # Can be used wherever a "file-like" object is accepted:
  df = pd.read_csv(uploaded_file)
  st.write(df)


#api_url = 'https://taxifare.lewagon.ai/predict'
#res = requests.get(api_url, params = df)

st.markdown("## Electiciryprediction:  🚕 ")
#st.write(res.text)
#data = res.json()

#for test graphs:
n = 20
api_res_df = pd.DataFrame({
    'lable_1': list(randint(0, 100, n)),
    'lable_2': list(randint(0, 100, n)),
    'lable_3': list(randint(0, 100, n))
})
