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


base = 'http://127.0.0.1:8000'
headers = {'Content-Type': 'application/json; charset=utf-8'}


def test_invalid_body_request():
    '''
    Test that the API returns a 400 error when called without a request body.
    '''
    url = base + '/v1/aderencia'

    response = requests.post(url, headers=headers)

    assert response.status_code == 400
    assert response.json()['error'].startswith('Invalid request body')


def test_invalid_body_schema():
    '''
    Test that the API returns a 400 error when called with an invalid request body schema.
    '''
    url = base + '/v1/aderencia'

    body = {'path': False}
    response = requests.post(url, json=body, headers=headers)

    assert response.status_code == 400
    assert response.json()['error'].startswith('Body schema is invalid')


def test_successful():
    '''
    Test that the API returns a successful response when called with a valid request body.
    '''
    url = base + '/v1/aderencia'
    body = {'path': './../datasets/credit_01/train.gz'}
    
    response = requests.post(url, json=body, headers=headers)

    assert response.status_code == 200
    
    response_body = response.json()
    assert isinstance(response_body['ks_test'], dict)
    assert isinstance(response_body['js_divergence'], float)
