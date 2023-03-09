import pickle
from collections import defaultdict
from datetime import datetime
import pandas as pd
import numpy as np
from typing import Dict
from sklearn.metrics import roc_auc_score


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
    body : dict
        A dictionary containing the input records.

    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame containing the formatted input records.

    '''
    
    df = pd.DataFrame.from_dict(body)

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

    with open('./../model.pkl', 'rb') as f:
        model = pickle.load(f)

    y_pred = model.predict_proba(X)[:, 1]    
    aucroc = roc_auc_score(y, y_pred)
    
    return aucroc
