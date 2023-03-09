import pickle
from collections import defaultdict
from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict, Tuple
from sklearn.metrics import roc_auc_score
from scipy.stats import ks_2samp
from scipy.spatial.distance import jensenshannon


def get_pre_trained_model(path: str = './../model.pkl'):
    with open(path, 'rb') as f:
            model = pickle.load(f)
    
    return model


def get_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    return df


def load_batch_records(path: str = './../batch_records.json') -> pd.DataFrame:
    df = pd.read_json(path)
    df.replace('', np.nan, inplace=True)
    df.fillna(value=np.nan, inplace=True)

    return df


def format_input_records(body: dict) -> pd.DataFrame:
    '''
    Formats the input records contained in a dictionary as a Pandas DataFrame.

    Parameters
    ----------
    body : list
        A list containing the input records.

    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame containing the formatted input records.

    '''
    
    df = pd.DataFrame(body)

    df.replace('', np.nan, inplace=True)
    df.fillna(value=np.nan, inplace=True)

    return df


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
    Calculates the area under the receiver operating characteristic (ROC) curve for the given input DataFrame.

    Parameters:
        input (pd.DataFrame): A Pandas DataFrame containing the input data. Must have a 'TARGET' column.

    Returns:
        float: The calculated AUCROC score.

    '''

    X = input.drop(['TARGET'], axis=1)
    y = input['TARGET']

    model = get_pre_trained_model()

    y_pred = model.predict_proba(X)[:, 1]
    aucroc = roc_auc_score(y, y_pred)
    
    return aucroc


def get_test_data() -> Tuple[pd.DataFrame, pd.Series]:
    df_test = pd.read_csv('./../datasets/credit_01/test.gz', compression='gzip')
    X = df_test.drop(['TARGET'], axis=1)
    y = df_test['TARGET']

    return X, y


def calculate_ks(path: str) -> Tuple[float, float]:
    '''
    Calculates the KS statistic and p-value for the predicted scores of a given model on the data in the path entry and test data.

    Parameters:
        path (str): The path to the data file.

    Returns:
        A tuple of the KS statistic and p-value.
    '''
    model = get_pre_trained_model()

    df_input = get_data(path)
    
    X = df_input.drop(['TARGET'], axis=1)
    X_test, _ = get_test_data()

    y_pred = model.predict_proba(X)[:, 1]
    y_pred_test = model.predict_proba(X_test)[:, 1]
    
    ks_statistic, p_value = ks_2samp(y_pred, y_pred_test)

    return ks_statistic, p_value


def calculate_js(path: str) -> float:
    '''
    Calculates the Jensen-Shannon (JS) distance between the probability distributions of a given model on the training and test data.

    Parameters:
        path (str): The path to the data file.

    Returns:
        The JS distance.
    '''
    model = get_pre_trained_model()

    df_input = get_data(path)
    X = df_input.drop(['TARGET'], axis=1)
    X_test, _ = get_test_data()

    y_pred = model.predict_proba(X)[:, 1]
    y_pred_test = model.predict_proba(X_test)[:, 1]

    hist1, _ = np.histogram(y_pred, bins=20, range=(0, 1), density=True)
    hist2, _ = np.histogram(y_pred_test, bins=20, range=(0, 1), density=True)

    js_distance = jensenshannon(hist1, hist2)

    return js_distance
