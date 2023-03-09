from jsonschema import validate
from api.endpoints.schemas.performance_body import BODY_SCHEMA


def validate_performance_body(body: dict):
    validate(instance=body, schema=BODY_SCHEMA)

def validate_aderencia_body(body: dict):

    validate(instance=body, schema={
        'type': 'object',
        'properties': {
                'path': {'type': 'string', 'pattern': '^\.\/\.\.\/\w+\/\w+_\d+\/\w+\.gz$'}
            },
        'required': ['path']
    })