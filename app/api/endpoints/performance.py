'''
Module that handles the /performance endpoint call.

The endpoint reads the model AUC-ROC performance using the body request as the input.
'''

from http import HTTPStatus
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from jsonschema import exceptions

from api.endpoints.utils import format_input_records, count_records_by_month, calculate_aucroc
from api.endpoints.validators import validate_performance_body
from api.endpoints.exceptions import InvalidRequestError, InternalServerError


router = APIRouter(prefix='/performance')


@router.post('')
async def read_performance(request: Request):
    '''
    Endpoint to read the model AUC-ROC performance using the body request as the input.

    Raises
    ----------
    InvalidRequestError
        If request body is not a valid JSON object or the
        body doesn't match the body schema.

    InternalServerError
        If an internal server error occurs.

    Returns
    ----------
    JSONResponse
        JSON response object containing the volumetry by month and the AUC-ROC value.
    '''

    try:
        body = await request.json()

        validate_performance_body(body)
    except ValueError as exception:
        raise InvalidRequestError(
            'Invalid request body. Must be a valid JSON object.') from exception
    except exceptions.ValidationError as exception:
        raise InvalidRequestError(
            f'Body schema is invalid: {exception.message}.') from exception

    try:
        df_input = format_input_records(body)
        records_by_month = count_records_by_month(df_input)
        auc_roc = calculate_aucroc(df_input)
    except Exception as exception:
        raise InternalServerError(str(exception)) from exception

    return JSONResponse(
        content={
            'volumetry': records_by_month,
            'auc_roc': auc_roc
        },
        status_code=HTTPStatus.OK
    )
