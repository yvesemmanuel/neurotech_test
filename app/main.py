'''
This module contains the FastAPI application for the models monitoring API.

It defines the root endpoint, includes the router, and sets up exception handlers.
'''


from http import HTTPStatus
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.routers import router

from api.endpoints.exceptions import InvalidRequestError, InternalServerError, InvalidPathError


app = FastAPI(title='Monitoramento de modelos', version='1.0.0')


@app.get('/')
async def root():
    '''
    Returns the root endpoint of the models monitoring API.

    Returns:
        A JSONResponse with a message indicating the root endpoint was reached.
    '''
    return JSONResponse(
        content={
            'message': 'models monitoring API root'
        },
        status_code=HTTPStatus.OK
    )


app.include_router(router, prefix='/v1')


@app.exception_handler(InvalidRequestError)
async def invalid_request_handler(_, exc):
    '''
    Exception handler for InvalidRequestError.

    Args:
        _: The request object
        exc: The exception object

    Returns:
        A JSONResponse with an error message and a BAD_REQUEST status code.
    '''
    return JSONResponse(
        content={'error': exc.message},
        status_code=HTTPStatus.BAD_REQUEST
    )


@app.exception_handler(InternalServerError)
async def internal_server_error_handler(_, exc):
    '''
    Exception handler for InternalServerError.

    Args:
        _: The request object
        exc: The exception object

    Returns:
        A JSONResponse with an error message and an INTERNAL_SERVER_ERROR status code.
    '''
    return JSONResponse(
        content={'error': exc.message},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    )


@app.exception_handler(InvalidPathError)
async def invalid_path_handler(_, exc):
    '''
    Exception handler for InvalidPathError.

    Args:
        _: The request object
        exc: The exception object

    Returns:
        A JSONResponse with an error message and a NOT_FOUND status code.
    '''
    return JSONResponse(
        content={'error': exc.message},
        status_code=HTTPStatus.NOT_FOUND
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
