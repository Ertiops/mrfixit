from dishka import Provider, Scope, provide

from mrfixit.domains.interfaces.storages.tech_request import ITechRequestStorage
from mrfixit.domains.services.tech_request import TechRequestService


class DomainProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def tech_request_service(
        self,
        *,
        tech_request_storage: ITechRequestStorage,
    ) -> TechRequestService:
        return TechRequestService(tech_request_storage=tech_request_storage)
