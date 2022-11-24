import pandas as pd
import numpy as np

from decipherer.ml_logic.encoders import ffill_nan, add_datetime_features

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
    y_pred = pipeline.predict(X_pred)

    print("\n✅ prediction done: ", y_pred, y_pred.shape)

    return y_pred

if __name__ == '__main__':
    pred()
