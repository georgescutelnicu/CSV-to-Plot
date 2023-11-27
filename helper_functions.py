import pandas as pd
import warnings


warnings.filterwarnings("ignore")

def preprocess_data(data):

    for col in data.columns:
        if data[col].dtype == 'object':
            try:
                data[col] = pd.to_datetime(data[col])
            except:
                pass

    return data