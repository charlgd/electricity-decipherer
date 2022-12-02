'''MODEL FOR V2 (APPLIANCE LEVEL) - STEP 1: USING CONSTANT KWH VALUES FOR EACH APPLIANCE'''
from sklearn.base import BaseEstimator
import pandas as pd

class ApplianceEstimator(BaseEstimator):

    def __init__(self, appliances_wh):
        self.appliances_wh = appliances_wh

    def predict(self, X, selected_appliances):

        appliances_wh_df = pd.DataFrame.from_dict(self.appliances_wh, orient='index', columns=['wh'])
        appliances_wh_df = appliances_wh_df.loc[selected_appliances]
        appliances_wh_df['pct'] = appliances_wh_df.wh / sum(appliances_wh_df.wh)

        y = X[['date_time']]
        for a in selected_appliances:
           y[a] = X.iloc[:, 1] * appliances_wh_df.loc[a, 'pct']

        return y
