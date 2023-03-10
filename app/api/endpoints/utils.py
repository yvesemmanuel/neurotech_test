'''
The utils module contains utility functions for handling internal operations in
the endpoints of a machine learning web service. 

Functions:
----------
- get_pre_trained_model(path: str) -> object:
    Returns the pre-trained machine learning model loaded from the given path.

- get_data(path: str) -> pd.DataFrame:
    Reads the CSV file from the given path and returns a Pandas dataframe.

- load_batch_records(path: str) -> pd.DataFrame:
    Load batch records data from a JSON file into a Pandas DataFrame.

- format_input_records(body: List[dict]) -> pd.DataFrame:
    Formats the input records (dict) contained in a list as a Pandas DataFrame.

- count_records_by_month(records: pd.DataFrame) -> Dict[str, int]:
    Counts the number of records by month in a given DataFrame.

- calculate_aucroc(input: pd.DataFrame) -> float:
    Calculates the area under the receiver operating characteristic (ROC) curve
    for the given input DataFrame.

- get_test_data() -> Tuple[pd.DataFrame, pd.Series]:
    Reads and loads test data from a gzip-compressed CSV file
    located at './../datasets/credit_01/test.gz'.

- calculate_ks(path: str) -> Tuple[float, float]:
    Calculates the KS statistic and p-value for the predicted scores of a given
    model on the data in the path entry and test data.

- calculate_js(path: str) -> float:
    Calculates the Jensen-Shannon (JS) distance between the probability
    distributions of a given model on the training and test data.
'''

import pickle
from collections import defaultdict
from datetime import datetime
from typing import Dict, Tuple, List
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
from scipy.stats import ks_2samp
from scipy.spatial.distance import jensenshannon


def get_pre_trained_model(path: str = './../model.pkl') -> object:
    '''
    Returns the pre-trained machine learning model loaded from the given path.

    Parameters
    ----------
    path : str
        The path to the pickle file containing the pre-trained model.

    Returns
    -------
    object
        An object representing the pre-trained machine learning model.
    '''
    with open(path, 'rb') as file:
        model = pickle.load(file)

    return model


def get_data(path: str) -> pd.DataFrame:
    '''
    Reads the CSV file from the given path and returns a Pandas dataframe.

    Parameters
    ----------
    path : str
        The path to the CSV file containing the data.

    Returns
    -------
    pd.DataFrame
        A Pandas dataframe containing the data.
    '''
    data_frame = pd.read_csv(path)

    return data_frame


def load_batch_records(path: str = './../batch_records.json') -> pd.DataFrame:
    '''
    Load batch records data from a JSON file into a Pandas DataFrame.

    Parameters
    ----------
    path : str
        The path to the JSON file containing the batch records data. Default is './../batch_records.json'.

    Returns
    ----------
    pd.DataFrame:
        The batch records data in a Pandas DataFrame.
    '''
    data_frame = pd.read_json(path)
    data_frame.replace('', np.nan, inplace=True)
    data_frame.fillna(value=np.nan, inplace=True)

    return data_frame


def format_input_records(body: List[dict]) -> pd.DataFrame:
    '''
    Formats the input records (dict) contained in a list as a Pandas DataFrame.

    Parameters
    ----------
    body : list
        A list containing the input records.

    Returns
    ----------
    pd.DataFrame
        A Pandas DataFrame containing the formatted input records.
    '''
    data_frame = pd.DataFrame(body)

    data_frame.replace('', np.nan, inplace=True)
    data_frame.fillna(value=np.nan, inplace=True)

    return data_frame


def count_records_by_month(records: pd.DataFrame) -> Dict[str, int]:
    '''
    Counts the number of records by month in a given DataFrame.

    Parameters:
    -----------
    records : pd.DataFrame
        The input DataFrame containing the records to be counted.

    Returns:
    --------
    Dict[str, int]
        A dictionary containing the count of records by month, where the key is a string
        in the format 'YYYY-MM' representing the year and month, and the value is the count
        of records for that month.
    '''
    counts = defaultdict(int)

    for _, record in records.iterrows():
        ref_date_str = record.get('REF_DATE')

        if isinstance(ref_date_str, str):
            ref_date = datetime.fromisoformat(ref_date_str[:-6])
            key = f'{ref_date.year}-{ref_date.month:02}'
            counts[key] += 1

    return dict(counts)


def calculate_aucroc(input: pd.DataFrame) -> float:
    '''
    Calculates the area under the receiver operating characteristic (ROC) curve
    for the given input DataFrame.

    Parameters
    ----------

    input : pd.DataFrame
        A Pandas DataFrame 
        containing the input data. Must have a 'TARGET' column.

    Returns
    ----------
    float
        The calculated AUCROC score.
    '''
    x_input = input.drop(['TARGET'], axis=1)
    y_input = input['TARGET']

    model = get_pre_trained_model()

    y_pred = model.predict_proba(x_input)[:, 1]
    aucroc = roc_auc_score(y_input, y_pred)

    return aucroc


def get_test_data() -> Tuple[pd.DataFrame, pd.Series]:
    '''
    Reads and loads test data from a gzip-compressed CSV file
    located at './../datasets/credit_01/test.gz'.

    Returns
    ----------
    A tuple with two elements:
        - X: a pandas DataFrame with the features of the test data.
        - y: a pandas Series with the target variable of the test data.
    '''
    df_test = pd.read_csv(
        './../datasets/credit_01/test.gz', compression='gzip')
    x_test = df_test.drop(['TARGET'], axis=1)
    y_test = df_test['TARGET']

    return x_test, y_test


def calculate_ks(path: str) -> Tuple[float, float]:
    '''
    Calculates the KS statistic and p-value for the predicted scores of a given model
    on the data in the path entry and test data.

    Parameters
    ----------
    path : str
        The path to the data file.

    Returns
    ----------
    A tuple of the KS statistic and p-value.
    '''
    model = get_pre_trained_model()

    df_input = get_data(path)

    x_input = df_input.drop(['TARGET'], axis=1)
    x_test, _ = get_test_data()

    y_pred = model.predict_proba(x_input)[:, 1]
    y_pred_test = model.predict_proba(x_test)[:, 1]

    ks_statistic, p_value = ks_2samp(y_pred, y_pred_test)

    return ks_statistic, p_value


def calculate_js(path: str) -> float:
    '''
    Calculates the Jensen-Shannon (JS) distance between the probability
    distributions of a given model on the training and test data.

    Parameters
    ----------
    path : str
        The path to the data file.

    Returns
    ----------
    The JS distance.
    '''
    model = get_pre_trained_model()

    df_input = get_data(path)
    x_input = df_input.drop(['TARGET'], axis=1)
    x_test, _ = get_test_data()

    y_pred = model.predict_proba(x_input)[:, 1]
    y_pred_test = model.predict_proba(x_test)[:, 1]

    hist1, _ = np.histogram(y_pred, bins=20, range=(0, 1), density=True)
    hist2, _ = np.histogram(y_pred_test, bins=20, range=(0, 1), density=True)

    js_distance = jensenshannon(hist1, hist2)

    return js_distance
