'''
validators.py

This module contains functions for validating API request bodies.

'''

from jsonschema import validate
from api.endpoints.schemas.performance_body import BODY_SCHEMA


def validate_performance_body(body: dict):
    '''
    Validates a performance API request body against a JSON schema.

    Parameters
    ----------
    body
        A dictionary representing the performance API request body.

    Raises
    ----------
    jsonschema.exceptions.ValidationError
        If the body is not valid.
    '''
    validate(instance=body, schema=BODY_SCHEMA)


def validate_adherence_body(body: dict):
    '''
    Validates an adherence API request body against a JSON schema.

    Parameters
    ----------
    body
        A dictionary representing the adherence API request body.

    Raises
    ----------
    jsonschema.exceptions.ValidationError
        If the body is not valid.
    '''
    validate(instance=body, schema={
        'type': 'object',
        'properties': {
                'path': {'type': 'string', 'pattern': '^\.\/\.\.\/\w+\/\w+_\d+\/\w+\.gz$'}
        },
        'required': ['path']
    })
