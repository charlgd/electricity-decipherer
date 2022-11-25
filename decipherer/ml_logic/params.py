"""
decipherer model package params
load and validate the environment variables in the `.env`
"""
import os

LOCAL_REGISTRY_PATH = "training_outputs"

# Google Cloud
PROJECT_NAME = os.environ.get("PROJECT")
