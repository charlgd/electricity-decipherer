import pandas as pd
import numpy as np

#from decipherer.ml_logic.encoders import ffill_nan, add_datetime_features

def room_pred(X_pred: pd.DataFrame = None) -> np.ndarray:
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ Use case: predict")

    from decipherer.ml_logic.registry import load_pipeline

    if X_pred is None:

        X_pred = pd.DataFrame(dict(
            date=["6/7/2008"],
            time=["17:18:00"],
            global_active_power=2.196,
            global_reactive_power=0.218,
            voltage=239.37,
            global_intensity=9.2,
            global_consumption=22.0
        ))

    pipeline = load_pipeline(pipeline_type='room')
    y_pred = pd.DataFrame(pipeline.predict(X_pred))
    y_pred['datetime'] = pd.to_datetime(X_pred['date'] + ' ' + X_pred['time'])

    print("\n✅ prediction done: ", y_pred.head(), y_pred.shape)

    return y_pred

if __name__ == '__main__':
    room_pred()
