from aiogram import Router
from .match_handlers import router as match_router
router = Router()
router.include_router(match_router)