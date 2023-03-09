import requests
import json


base = 'http://127.0.0.1:8000'
headers = {'Content-Type': 'application/json; charset=utf-8'}

def test_invalid_body_request():
    url = base + '/v1/performance'

    response = requests.post(url, headers=headers)

    assert response.status_code == 400
    assert response.json()['error'].startswith('Invalid request body')


def test_invalid_body_schema():
    url = base + '/v1/performance'

    body = get_testing_body()
    first_record = body[0]

    response = requests.post(url, json=first_record, headers=headers)

    assert response.status_code == 400
    assert response.json()['error'].startswith('Body schema is invalid')


def test_successful():
    url = base + '/v1/performance'
    
    body = get_testing_body()
    response = requests.post(url, json=body, headers=headers)

    assert response.status_code == 200

    response_body = response.json()
    assert isinstance(response_body['volumetry'], dict)
    assert isinstance(response_body['auc_roc'], float)


def get_testing_body(path: str = './../batch_records.json'):
    with open(path) as f:
        body = json.load(f)

    return body