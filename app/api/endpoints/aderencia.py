from fastapi import APIRouter

router = APIRouter(prefix="/aderencia")

@router.get('/aderencia')
def read_aderencia():
    return {'message': 'This is the aderencia endpoint!'}