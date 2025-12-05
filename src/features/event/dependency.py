"""
Contenedor de Inyección de Dependencias para el feature de Event
"""
from functools import lru_cache
from src.features.event.domain.port.Ievent_repository import EventRepositoryPort
from src.features.event.infrastructure.event_repository import EventRepository
from src.features.event.application.uses_cases.create_event import CreateEventUseCase

from src.features.event.application.uses_cases.get_events_by_user import GetEventsByUserUseCase

from src.features.event.application.uses_cases.register_user_to_event import RegisterUserToEventUseCase


class EventDependencyContainer:
    _instance = None
    _event_repository: EventRepositoryPort = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_event_repository(self) -> EventRepositoryPort:
        if self._event_repository is None:
            self._event_repository = EventRepository()
        return self._event_repository
    
    def get_create_event_use_case(self) -> CreateEventUseCase:
        """Retorna una instancia del caso de uso de crear evento"""
        return CreateEventUseCase(event_repository=self.get_event_repository())

    def get_register_user_to_event_use_case(self) -> RegisterUserToEventUseCase:
        """Retorna una instancia del caso de uso de registrar usuario a evento"""
        return RegisterUserToEventUseCase(event_repository=self.get_event_repository())

    def get_events_by_user_id_use_case(self) -> GetEventsByUserUseCase:
        """Retorna una instancia del caso de uso de obtener eventos por usuario"""
        return GetEventsByUserUseCase(event_repository=self.get_event_repository())


# Función helper para FastAPI Depends
@lru_cache()
def get_dependency_container() -> EventDependencyContainer:
    return EventDependencyContainer()


# Funciones de dependencia para FastAPI
def get_event_repository_dependency() -> EventRepositoryPort:
    """Dependencia para inyectar el repositorio de eventos"""
    container = get_dependency_container()
    return container.get_event_repository()


def get_create_event_use_case_dependency() -> CreateEventUseCase:
    """Dependencia para inyectar el caso de uso de crear evento"""
    container = get_dependency_container()
    return container.get_create_event_use_case()

def get_register_user_to_event_use_case_dependency() -> RegisterUserToEventUseCase:
    """Dependencia para inyectar el caso de uso de registrar usuario a evento"""
    container = get_dependency_container()
    return container.get_register_user_to_event_use_case()

def get_events_by_user_id_use_case_dependency() -> GetEventsByUserUseCase:
    """Dependencia para inyectar el caso de uso de obtener eventos por usuario"""
    container = get_dependency_container()
    return container.get_events_by_user_id_use_case()

