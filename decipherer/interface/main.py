import pandas as pd
import numpy as np

def pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ Use case: predict")

    from decipherer.ml_logic.registry import load_pipeline

    if X_pred is None:

        X_pred = pd.DataFrame(dict(
            date=["2008-07-06"],
            time=["17:18:00"],
            global_active_power=2.196,
            global_reactive_power=0.218,
            voltage=239.37,
            global_intensity=9.2,
            global_consumption=22.0
        ))

    pipeline = load_pipeline()

    y_pred = pd.DataFrame(pipeline.predict(X_pred))

    y_pred.columns = ['kitchen', 'laundry_room', 'heating_room']
    y_pred['date_time'] = pd.to_datetime(X_pred['date'] + ' ' + X_pred['time'], format="%d/%m/%Y %H:%M:%S")

    print("\n✅ prediction done: ", y_pred.head(), y_pred.shape)

    return y_pred

if __name__ == '__main__':

    # Test data
    # X_pred = pd.DataFrame({
    #     'date': ['1/1/2010', '2/1/2010', '30/1/2010'],
    #     'time': ['00:15:00', '10:20:00', '13:50:00'],
    #     'global_active_power': [10, 10, 10],
    #     'global_reactive_power': [10, 10, 10],
    #     'voltage': [10, 10, 10],
    #     'global_intensity': [10, 10, 10],
    #     'global_consumption': [10, 10, 10]
    # })

    pred()
