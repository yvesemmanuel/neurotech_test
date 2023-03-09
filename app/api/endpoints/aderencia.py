from http import HTTPStatus
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from api.endpoints.utils import calculate_ks, calculate_js

from jsonschema import exceptions
from api.endpoints.validators import validate_aderencia_body
from api.endpoints.exceptions import InvalidRequestError, InternalServerError, InvalidPathError


router = APIRouter(prefix='/aderencia')


@router.post('')
async def read_aderencia(request: Request):
    try:
        body = await request.json()

        validate_aderencia_body(body)
    except ValueError:
        raise InvalidRequestError(
            'Invalid request body. Must be a valid JSON object.')
    except exceptions.ValidationError as e:
        raise InvalidRequestError(
            'Body schema is invalid: {}.'.format(e.message))

    try:
        ks_statistic, p_value = calculate_ks(body['path'])
        js_distance = calculate_js(body['path'])
    except FileNotFoundError as e:
        raise InvalidPathError(
            'No such file or directory in the provide path.')
    except Exception as e:
        raise InternalServerError(str(e))

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
