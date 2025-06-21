import logging
from datetime import datetime, timedelta

from aiomisc.service.cron import CronService
from dishka import make_async_container

from mrfixit.adapters.database.di import DatabaseProvider
from mrfixit.config import MainConfig
from mrfixit.domains.di import DomainProvider
from mrfixit.domains.entities.tech_request import (
    DeleteTechRequsetList,
    TechRequestStatus,
)
from mrfixit.domains.services.tech_request import TechRequestService
from mrfixit.domains.uow import AbstractUow

log = logging.getLogger(__name__)


class TechRequestCronService(CronService):
    __required__ = ("config",)
    config: MainConfig

    async def start(self) -> None:
        self.__add_dependency_overrides()
        self.register(self.delete_list, spec="0 0 * * *")
        await super().start()

    async def delete_list(self) -> None:
        async with self.__container() as container:
            uow: AbstractUow = await container.get(AbstractUow)
            service: TechRequestService = await container.get(TechRequestService)
            threshold_date = datetime.now() - timedelta(days=7)
            async with uow:
                await service.delete_list(
                    input_dto=DeleteTechRequsetList(
                        created_at=threshold_date,
                        status=TechRequestStatus.DONE,
                    )
                )
        log.info("TechRequests Are Successfully deleted: %s", threshold_date)

    def __add_dependency_overrides(self) -> None:
        self.__container = make_async_container(
            DatabaseProvider(self.config.db),
            DomainProvider(),
            skip_validation=True,
        )
