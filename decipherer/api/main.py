from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Union
from decipherer.ml_logic.registry import load_pipeline
import pandas as pd
import json
import os

app = FastAPI()
app.state.pipeline = load_pipeline()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Item(BaseModel):
    date: Union[str, None] = None
    time: Union[str, None] = None
    global_active_power: Union[float, None] = None
    global_reactive_power: Union[float, None] = None
    voltage: Union[float, None] = None
    global_intensity: Union[float, None] = None
    global_consumption: Union[float, None] = None

@app.post("/")
async def index(items: List[Item]):

     # Check for the env
    if (os.environ.get('APP_ENV') == 'development'):

        # Receive body in the request
        body = [item.dict() for item in items]

        # Convert body to pandas dataframe
        X_pred = pd.DataFrame(body, columns=['date', 'time', 'global_active_power', 'global_reactive_power', 'voltage', 'global_intensity', 'global_consumption'])

        print("body")

        # Load pipeline from app.state
        pipeline = app.state.pipeline

        y_pred = pd.DataFrame(pipeline.predict(X_pred))

        y_pred.columns = ['kitchen', 'laundry_room', 'heating_room']
        y_pred['date_time'] = pd.to_datetime(X_pred['date'] + ' ' + X_pred['time'], format="%d/%m/%Y %H:%M:%S").astype(str)

        # # Convert dataframe to json
        y_pred_json = y_pred.to_json(orient="records")

        return JSONResponse(status_code=status.HTTP_200_OK, content=json.loads(y_pred_json))
