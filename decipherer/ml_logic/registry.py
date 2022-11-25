from colorama import Fore, Style
from sklearn.pipeline import Pipeline
from joblib import dump, load

import time
import os
import glob
import pickle

from decipherer.ml_logic.params import LOCAL_REGISTRY_PATH


def save_pipeline(pipeline: Pipeline = None,
                  params: dict = None,
                  metrics: dict = None) -> None:
    """
    persist trained pipeline, params and metrics
    """

    timestamp = time.strftime("%Y%m%d-%H%M%S")

    print(Fore.BLUE + "\nSave pipeline to local disk..." + Style.RESET_ALL)

    # save params
    if params is not None:
        params_path = os.path.join(LOCAL_REGISTRY_PATH, "params", timestamp + ".pickle")
        with open(params_path, "wb") as file:
            pickle.dump(params, file)

    # save metrics
    if metrics is not None:
        metrics_path = os.path.join(LOCAL_REGISTRY_PATH, "metrics", timestamp + ".pickle")
        with open(metrics_path, "wb") as file:
            pickle.dump(metrics, file)

    # save pipeline
    if pipeline is not None:
        pipeline_path = os.path.join(LOCAL_REGISTRY_PATH, "models", timestamp + ".joblib")
        dump(pipeline, pipeline_path)

    print("\n✅ data saved locally")

    return None


def load_pipeline() -> Pipeline:
    """
    load the latest saved pipeline, return None if no model found
    """
    print(Fore.BLUE + "\nLoad pipeline from local disk..." + Style.RESET_ALL)

    pipeline_directory = os.path.join(LOCAL_REGISTRY_PATH, "models")

    results = glob.glob(f"{pipeline_directory}/*")
    if not results:
        return None

    pipeline_path = sorted(results)[-1]
    print(f"- path: {pipeline_path}")
    #breakpoint()
    pipeline = load(pipeline_path)
    print("\n✅ pipeline loaded from disk")

    return pipeline
