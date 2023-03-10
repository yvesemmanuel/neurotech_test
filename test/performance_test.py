'''
This module contains tests for the performance endpoint of the API.

The performance endpoint is responsible for analyzing the performance of a machine learning model based on a set of batch records.

Functions:
----------
test_invalid_body_request():
    Tests the behavior of the endpoint when an invalid request body is sent.

test_invalid_body_schema():
    Tests the behavior of the endpoint when an invalid body schema is sent.

test_successful():
    Tests the successful behavior of the endpoint when a valid request body is sent.

get_testing_body(path: str = './../batch_records.json'):
    Helper function that returns a testing batch records body.
'''

import requests
import json


base = 'http://127.0.0.1:8000'
headers = {'Content-Type': 'application/json; charset=utf-8'}


def test_invalid_body_request():
    '''
    Test the behavior of the performance endpoint when an invalid request body is sent.
    '''
    url = base + '/v1/performance'

    response = requests.post(url, headers=headers)

    assert response.status_code == 400
    assert response.json()['error'].startswith('Invalid request body')


def test_invalid_body_schema():
    '''
    Test the behavior of the performance endpoint when an invalid body schema is sent.
    '''
    url = base + '/v1/performance'

    body = get_testing_body()
    first_record = body[0]

    response = requests.post(url, json=first_record, headers=headers)

    assert response.status_code == 400
    assert response.json()['error'].startswith('Body schema is invalid')


def test_successful():
    '''
    Test the successful behavior of the performance endpoint when a valid request body is sent.
    '''
    url = base + '/v1/performance'
    
    body = get_testing_body()
    response = requests.post(url, json=body, headers=headers)

    assert response.status_code == 200

    response_body = response.json()
    assert isinstance(response_body['volumetry'], dict)
    assert isinstance(response_body['auc_roc'], float)


def get_testing_body(path: str = './../batch_records.json'):
    '''
    Helper function that returns a testing batch records body.

    Parameters:
    -----------
    path: str
        The path of the file containing the batch records body.

    Returns:
    --------
    The batch records body in JSON format.
    '''
    with open(path) as f:
        body = json.load(f)

    return body
