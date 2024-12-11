from dependency_injector import containers, providers

from breeze_bot.handlers.bid_categories import BidCategoriesHandler
from breeze_bot.infra.database.session import async_session_factory
from breeze_bot.handlers.bids import BidsHandler
from breeze_bot.handlers.employees import EmployeesHandler
from breeze_bot.repository.bid_categories import BidCategoriesRepository
from breeze_bot.repository.bids import BidsRepository
from breeze_bot.repository.employees import EmployeesRepository
from breeze_bot.repository.managers import ManagersRepository
from breeze_bot.repository.positions import PositionsRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            'breeze_bot.app.routers.bids',
            'breeze_bot.app.routers.employees',
            'breeze_bot.app.routers.positions',
            'breeze_bot.app.routers.managers',
            'breeze_bot.app.routers.bid_categories',
        ]
    )

    session_factory = providers.Singleton(async_session_factory)

    bids_repository = providers.Singleton(BidsRepository, session_factory=session_factory)
    employees_repository = providers.Singleton(EmployeesRepository, session_factory=session_factory)
    positions_repository = providers.Singleton(PositionsRepository, session_factory=session_factory)
    managers_repository = providers.Singleton(ManagersRepository, session_factory=session_factory)
    bid_categories_repository = providers.Singleton(BidCategoriesRepository, session_factory=session_factory)


    bids_handler = providers.Singleton(BidsHandler, bids_repository=bids_repository)
    employees_handler = providers.Singleton(EmployeesHandler, employees_repository=employees_repository)
    positions_handler = providers.Singleton(PositionsRepository, positions_repository=positions_repository)
    managers_handler = providers.Singleton(ManagersRepository, managers_repository=managers_repository)
    bid_categories_handler = providers.Singleton(
        BidCategoriesHandler, bid_categories_repository=bid_categories_repository
    )
