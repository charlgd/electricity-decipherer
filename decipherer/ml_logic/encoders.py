import pandas as pd
import numpy as np

def ffill_nan(X):
    '''Get rid of nan values using ffil'''
    return X.fillna(method='ffill', axis = 0)

def add_datetime_features(X):
    '''Create new datetime features'''

    # Copy X to avoid pandas warning
    X_rep = X.copy()

    # Handle datetime format
    datetime = pd.to_datetime(X_rep['date'] + ' ' + X_rep['time'])

    # Create new features using month, weekday, hour and minute
    X_rep['month'] = datetime.dt.month
    X_rep['weekday'] = datetime.dt.weekday
    X_rep['hour'] = datetime.dt.hour
    X_rep['minute'] = datetime.dt.minute

    # Consider periodic effects
    X_rep['month_sin'] = np.sin(2*np.pi*X_rep['month']/12)
    X_rep['month_cos'] = np.cos(2*np.pi*X_rep['month']/12)

    # Get rid of Datetime
    return X_rep.drop(columns=['date', 'time'])
