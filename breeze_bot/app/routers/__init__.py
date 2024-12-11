from fastapi import APIRouter

from breeze_bot.app.routers.bids import router as bids_router
from breeze_bot.app.routers.employees import router as employees_router
from breeze_bot.app.routers.positions import router as positions_router
from breeze_bot.app.routers.managers import router as managers_router
from breeze_bot.app.routers.bid_categories import router as bid_categories_router


router = APIRouter()

router.include_router(bids_router)
router.include_router(employees_router)
router.include_router(positions_router)
router.include_router(managers_router)
router.include_router(bid_categories_router)
