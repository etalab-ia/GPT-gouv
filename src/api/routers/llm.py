
from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_500_INTERNAL_SERVER_ERROR



router = APIRouter()


def get_random_result():
    return {'answer':'Désolé je n\'arrive pas à me mettre à votre niveau.'}


@router.post("/chat")
def reform_fake(prompt: str):
    return get_random_result()

@router.get("/clear_cache")
def clear_cache_db(secret: str):
    return {'cache_cleared':'ok'}
