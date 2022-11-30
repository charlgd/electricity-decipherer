'''MODEL FOR V2 (APPLIANCE LEVEL) - STEP 1: USING CONSTANT PERCENTAGES'''
from sklearn.base import BaseEstimator

class ApplianceEstimator(BaseEstimator):

    def __init__(self, appliances_pct):
        self.appliances_pct = appliances_pct

    def predict(self, X):

        y = X[['date_time']]

        for appliance, pct in self.appliances_pct.items():
           y[appliance] = X.iloc[:, 1] * pct

        return y
