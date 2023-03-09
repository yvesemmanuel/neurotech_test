import uvicorn
from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.routers import router

from api.endpoints.exceptions import InvalidRequestError, InternalServerError


app = FastAPI(title='Monitoramento de modelos', version='1.0.0')

@app.get('/')
def read_root():
    '''Hello World message.'''
    return {'Hello World': 'from FastAPI'}

app.include_router(router, prefix='/v1')

@app.exception_handler(InvalidRequestError)
async def invalid_request_handler(request, exc):
    return JSONResponse(
        content={'error': exc.message},
        status_code=HTTPStatus.BAD_REQUEST
    )


@app.exception_handler(InternalServerError)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        content={'error': exc.message},
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
