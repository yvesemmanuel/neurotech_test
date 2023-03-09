from http import HTTPStatus
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from jsonschema import validate, exceptions
from api.endpoints.utils import format_input_records, count_records_by_month, calculate_aucroc
from api.endpoints.exceptions import InvalidRequestError, InternalServerError


RECORD_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "VAR2": {"type": ["string", "null"]},
        "IDADE": {"type": ["number", "null"]},
        "VAR5": {"type": ["string", "null"]},
        "VAR6": {"type": ["number", "null"]},
        "VAR7": {"type": ["number", "null"]},
        "VAR8": {"type": ["string", "null"]},
        "VAR9": {"type": ["string", "null"]},
        "VAR10": {"type": ["string", "null"]},
        "VAR11": {"type": ["number", "null"]},
        "VAR12": {"type": ["number", "null"]},
        "VAR14": {"type": ["number", "null"]},
        "VAR15": {"type": ["number", "null"]},
        "VAR16": {"type": ["null", "number"]},
        "VAR18": {"type": ["number", "null"]},
        "VAR19": {"type": ["number", "null"]},
        "VAR22": {"type": ["number", "null"]},
        "VAR24": {"type": ["number", "null"]},
        "VAR25": {"type": ["number", "null"]},
        "VAR32": {"type": ["string", "null"]},
        "VAR39": {"type": ["number", "null"]},
        "VAR40": {"type": ["number", "null"]},
        "VAR41": {"type": ["number", "null"]},
        "VAR42": {"type": ["number", "null"]},
        "VAR47": {"type": ["number", "null"]},
        "VAR49": {"type": ["string", "null"]},
        "VAR50": {"type": ["string", "null"]},
        "VAR51": {"type": ["string", "null"]},
        "VAR52": {"type": ["string", "null"]},
        "VAR53": {"type": ["string", "null"]},
        "VAR54": {"type": ["string", "null"]},
        "VAR55": {"type": ["string", "null"]},
        "VAR56": {"type": ["string", "null"]},
        "VAR57": {"type": ["string", "null"]},
        "VAR58": {"type": ["string", "null"]},
        "VAR59": {"type": ["string", "null"]},
        "VAR60": {"type": ["string", "null"]},
        "VAR61": {"type": ["string", "null"]},
        "VAR62": {"type": ["string", "null"]},
        "VAR63": {"type": ["string", "null"]},
        "VAR64": {"type": ["string", "null"]},
        "VAR65": {"type": ["string", "null"]},
        "VAR66": {"type": ["string", "null"]},
        "VAR67": {"type": ["string", "null"]},
        "VAR68": {"type": ["string", "null"]},
        "VAR69": {"type": ["string", "null"]},
        "VAR70": {"type": ["string", "null"]},
        "VAR71": {"type": ["string", "null"]},
        "VAR72": {"type": ["string", "null"]},
        "VAR73": {"type": ["string", "null"]},
        "VAR74": {"type": ["string", "null"]},
        "VAR75": {"type": ["string", "null"]},
        "VAR76": {"type": ["string", "null"]},
        "VAR77": {"type": ["string", "null"]},
        "VAR78": {"type": ["string", "null"]},
        "VAR79": {"type": ["string", "null"]},
        "VAR80": {"type": ["string", "null"]},
        "VAR81": {"type": ["string", "null"]},
        "VAR82": {"type": ["string", "null"]},
        "VAR83": {"type": ["string", "null"]},
        "VAR84": {"type": ["string", "null"]},
        "VAR85": {"type": ["string", "null"]},
        "VAR86": {"type": ["string", "null"]},
        "VAR87": {"type": ["string", "null"]},
        "VAR88": {"type": ["string", "null"]},
        "VAR89": {"type": ["string", "null"]},
        "VAR90": {"type": ["string", "null"]},
        "VAR91": {"type": ["string", "null"]},
        "VAR92": {"type": ["string", "null"]},
        "VAR93": {"type": ["string", "null"]},
        "VAR94": {"type": ["string", "null"]},
        "VAR95": {"type": ["string", "null"]},
        "VAR96": {"type": ["string", "null"]},
        "VAR97": {"type": ["string", "null"]},
        "VAR98": {"type": ["string", "null"]},
        "VAR99": {"type": ["string", "null"]},
        "VAR100": {"type": ["string", "null"]},
        "VAR101": {"type": ["string", "null"]},
        "VAR102": {"type": ["string", "null"]},
        "VAR103": {"type": ["string", "null"]},
        "VAR104": {"type": ["string", "null"]},
        "VAR105": {"type": ["string", "null"]},
        "VAR106": {"type": ["string", "null"]},
        "VAR107": {"type": ["string", "null"]},
        "VAR108": {"type": ["string", "null"]},
        "VAR109": {"type": ["string", "null"]},
        "VAR110": {"type": ["string", "null"]},
        "VAR111": {"type": ["string", "null"]},
        "VAR112": {"type": ["string", "null"]},
        "VAR113": {"type": ["string", "null"]},
        "VAR114": {"type": ["string", "null"]},
        "VAR115": {"type": ["string", "null"]},
        "VAR116": {"type": ["string", "null"]},
        "VAR117": {"type": ["string", "null"]},
        "VAR118": {"type": ["string", "null"]},
        "VAR119": {"type": ["string", "null"]},
        "VAR120": {"type": ["string", "null"]},
        "VAR121": {"type": ["string", "null"]},
        "VAR122": {"type": ["string", "null"]},
        "VAR123": {"type": ["string", "null"]},
        "VAR124": {"type": ["string", "null"]},
        "VAR125": {"type": ["string", "null"]},
        "VAR126": {"type": ["string", "null"]},
        "VAR127": {"type": ["string", "null"]},
        "VAR128": {"type": ["string", "null"]},
        "VAR129": {"type": ["string", "null"]},
        "VAR130": {"type": ["string", "null"]},
        "VAR131": {"type": ["string", "null"]},
        "VAR132": {"type": ["string", "null"]},
        "VAR133": {"type": ["string", "null"]},
        "VAR134": {"type": ["string", "null"]},
        "VAR135": {"type": ["string", "null"]},
        "VAR136": {"type": ["string", "null"]},
        "VAR137": {"type": ["string", "null"]},
        "VAR138": {"type": ["string", "null"]},
        "VAR139": {"type": ["string", "null"]},
        "VAR140": {"type": ["string", "null"]},
        "VAR141": {"type": ["number", "null"]},
        "VAR142": {"type": ["string", "null"]},
        "REF_DATE": {"type": "string", "format": "date-time"},
        "TARGET": {"type": "number"}
    },
    'required': ['VAR2', 'IDADE', 'VAR5', 'VAR6', 'VAR7', 'VAR8', 'VAR9', 'VAR10', 'VAR11', 'VAR12', 'VAR14', 'VAR15', 'VAR16', 'VAR18', 'VAR19', 'VAR22', 'VAR24', 'VAR25', 'VAR32', 'VAR39', 'VAR40', 'VAR41', 'VAR42', 'VAR47', 'VAR49', 'VAR50', 'VAR51', 'VAR52', 'VAR53', 'VAR54', 'VAR55', 'VAR56', 'VAR57', 'VAR58', 'VAR59', 'VAR60', 'VAR61', 'VAR62', 'VAR63', 'VAR64', 'VAR65', 'VAR66', 'VAR67', 'VAR68', 'VAR69', 'VAR70', 'VAR71', 'VAR72', 'VAR73', 'VAR74', 'VAR75', 'VAR76', 'VAR77', 'VAR78', 'VAR79', 'VAR80', 'VAR81', 'VAR82', 'VAR83', 'VAR84', 'VAR85', 'VAR86', 'VAR87', 'VAR88', 'VAR89', 'VAR90', 'VAR91', 'VAR92', 'VAR93', 'VAR94', 'VAR95', 'VAR96', 'VAR97', 'VAR98', 'VAR99', 'VAR100', 'VAR101', 'VAR102', 'VAR103', 'VAR104', 'VAR105', 'VAR106', 'VAR107', 'VAR108', 'VAR109', 'VAR110', 'VAR111', 'VAR112', 'VAR113', 'VAR114', 'VAR115', 'VAR116', 'VAR117', 'VAR118', 'VAR119', 'VAR120', 'VAR121', 'VAR122', 'VAR123', 'VAR124', 'VAR125', 'VAR126', 'VAR127', 'VAR128', 'VAR129', 'VAR130', 'VAR131', 'VAR132', 'VAR133', 'VAR134', 'VAR135', 'VAR136', 'VAR137', 'VAR138', 'VAR139', 'VAR140', 'VAR141', 'VAR142', 'REF_DATE', 'TARGET']
}

router = APIRouter(prefix='/performance')

@router.post('')
async def read_performance(request: Request):
    '''
    Endpoint to read the model AUC-ROC performance using the body request as the input.
    
    Raises:
        InvalidRequestError: If request body is not a valid JSON object or the body doesn't match the input schema.
        InternalServerError: If an internal server error occurs.

    Returns:
        JSONResponse: JSON response object containing the volumetry by month and the AUC-ROC value.
    '''

    try:
        body = await request.json()

        for record in body:
            validate(instance=record, schema=RECORD_SCHEMA)
    except ValueError:
        raise InvalidRequestError('Invalid request body. Must be a valid JSON object.')
    except exceptions.ValidationError as e:
        raise InvalidRequestError('Body schema is invalid: {}.'.format(e.message))

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
