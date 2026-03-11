from fastapi import APIRouter
from .endpoints import query

api_router = APIRouter(prefix="/api/v1", tags=["v1"])
api_router.include_router(query.router)
