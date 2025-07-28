from fastapi import APIRouter

from app.api.routes import (
    auth,
    utils,
    tweets,
    users,
)


api_router = APIRouter()
api_router.include_router(utils.router)
api_router.include_router(tweets.router)
api_router.include_router(users.router)
api_router.include_router(auth.router)
