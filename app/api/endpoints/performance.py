from http import HTTPStatus
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from api.endpoints.utils import format_input_records, count_records_by_month, calculate_aucroc
from api.endpoints.exceptions import InvalidRequestError, InternalServerError


router = APIRouter(prefix='/performance')

@router.post('')
async def read_performance(request: Request):
    '''
    Endpoint to read the model AUC-ROC performance using the body request as the input.
    
    Raises:
        InvalidRequestError: If request body is not a valid JSON object.
        InternalServerError: If an internal server error occurs.

    Returns:
        JSONResponse: JSON response object containing the volumetry by month and the AUC-ROC value.
    '''

    try:
        body = await request.json()
    except ValueError:
        raise InvalidRequestError('Invalid request body. Must be a valid JSON object.')

    try:
        df = format_input_records(body)
        records_by_month = count_records_by_month(df)
        auc_roc = calculate_aucroc(df)
    except Exception as e:
        raise InternalServerError(str(e))

    return JSONResponse(
        content={
            'volumetry': records_by_month,
            'auc_roc': auc_roc
        },
        status_code=HTTPStatus.OK
    )
