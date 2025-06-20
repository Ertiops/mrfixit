from collections.abc import AsyncIterator

from dishka import AnyOf, BaseScope, Component, Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from mrfixit.adapters.database.config import DatabaseConfig
from mrfixit.adapters.database.storages.tech_request import TechRequestStorage
from mrfixit.adapters.database.uow import SqlalchemyUow
from mrfixit.adapters.database.utils import create_engine, create_sessionmaker
from mrfixit.domains.interfaces.storages.tech_request import ITechRequestStorage
from mrfixit.domains.uow import AbstractUow


class DatabaseProvider(Provider):
    def __init__(
        self,
        config: DatabaseConfig,
        scope: BaseScope | None = None,
        component: Component | None = None,
    ) -> None:
        self.dsn = config.dsn
        self.debug = config.debug
        super().__init__(scope=scope, component=component)

    @provide(scope=Scope.APP)
    async def engine(self) -> AsyncIterator[AsyncEngine]:
        async with create_engine(dsn=self.dsn, debug=self.debug) as engine:
            yield engine

    @provide(scope=Scope.APP)
    def session_factory(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_sessionmaker(engine=engine)

    @provide(scope=Scope.REQUEST)
    def uow(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AnyOf[SqlalchemyUow, AbstractUow]:
        return SqlalchemyUow(session=session_factory())

    @provide(scope=Scope.REQUEST)
    def tech_request_storage(self, uow: SqlalchemyUow) -> ITechRequestStorage:
        return TechRequestStorage(session=uow.session)
