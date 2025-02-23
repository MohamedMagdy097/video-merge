from fastapi import APIRouter
from video_merge.routers import merge
# contains all the routes under /api
router = APIRouter(prefix="/api")

# core routes
router.include_router(router=merge.router)

