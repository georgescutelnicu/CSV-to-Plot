import pandas as pd
import warnings


warnings.filterwarnings("ignore")


def preprocess_data(data):
    """
        Preprocesses a DataFrame by converting object-type columns to datetime.

        This function iterates through each column in the DataFrame and attempts to convert
        columns with 'object' dtype to datetime using pd.to_datetime. Columns that cannot be
        converted are left unchanged.

        Parameters:
            data (pd.DataFrame): The input DataFrame to be preprocessed.

        Returns:
            pd.DataFrame: The preprocessed DataFrame with datetime conversion applied to
                          eligible columns.
    """
    for col in data.columns:
        if data[col].dtype == 'object':
            try:
                data[col] = pd.to_datetime(data[col])
            except:
                pass

    return data
