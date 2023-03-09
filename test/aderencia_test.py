import requests


base = 'http://127.0.0.1:8000'
headers = {'Content-Type': 'application/json; charset=utf-8'}

def test_invalid_body_request():
    url = base + '/v1/aderencia'

    response = requests.post(url, headers=headers)

    assert response.status_code == 400
    assert response.json()['error'].startswith('Invalid request body')


def test_invalid_body_schema():
    url = base + '/v1/aderencia'

    body = {'path': False}
    response = requests.post(url, json=body, headers=headers)

    assert response.status_code == 400
    assert response.json()['error'].startswith("Body schema is invalid")


def test_successful():
    url = base + '/v1/aderencia'
    body = {'path': './../datasets/credit_01/train.gz'}
    
    response = requests.post(url, json=body, headers=headers)

    assert response.status_code == 200
    
    response_body = response.json()
    assert isinstance(response_body['ks_test'], dict)
    assert isinstance(response_body['js_divergence'], float)
