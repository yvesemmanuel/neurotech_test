'''
Module that handles the /aderencia endpoint call.

The endpoint reads the adherence statistics Kolmogorov-Smirnov (KS) test and
Jensen-Shannon (JS)divergence for the dataset located in
the path passed in the request body and the test dataset.
'''


from http import HTTPStatus
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from jsonschema import exceptions


from api.endpoints.utils import calculate_ks, calculate_js
from api.endpoints.validators import validate_adherence_body
from api.endpoints.exceptions import InvalidRequestError, InternalServerError, InvalidPathError


router = APIRouter(prefix='/aderencia')


@router.post('')
async def read_adherence(request: Request):
    '''
    Endpoint to read the adherence statistics Kolmogorov-Smirnov (KS) test and
    Jensen-Shannon (JS) divergence for the dataset located in the path
    passed in the request body and the test dataset.

    Raises
    ----------
    InvalidRequestError
        If the request body is not a valid JSON object.
    InvalidPathError
        If the provided path does not exist.
    InternalServerError
        If an unexpected error occurs during the execution.

    Returns
    ----------
    JSONResponse
        A JSON object containing the KS and JS statistical tests.
    '''

    try:
        body = await request.json()

        validate_adherence_body(body)
    except ValueError as exception:
        raise InvalidRequestError(
            'Invalid request body. Must be a valid JSON object.') from exception
    except exceptions.ValidationError as exception:
        raise InvalidRequestError(
            f'Body schema is invalid: {exception.message}.') from exception

    try:
        ks_statistic, p_value = calculate_ks(body['path'])
        js_distance = calculate_js(body['path'])
    except FileNotFoundError as exception:
        raise InvalidPathError(
            'No such file or directory in the provide path.') from exception
    except Exception as exception:
        raise InternalServerError(str(exception)) from exception

    return JSONResponse(
        content={
            'ks_test': {
                'ks_statistic': ks_statistic,
                'p_value': p_value
            },
            'js_divergence': js_distance
        },
        status_code=HTTPStatus.OK
    )
