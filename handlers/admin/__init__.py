from aiogram import Router

router = Router()

from .start import router as start_router

router.include_router(start_router)

from .client import router as client_router

router.include_router(client_router)