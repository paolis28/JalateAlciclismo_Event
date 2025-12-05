from abc import ABC, abstractmethod
from typing import List, Optional
from src.features.event.domain.entities.event import Event

class EventRepositoryPort(ABC):
    @abstractmethod
    def create_event(self, event_data: Event):
        """Crear un nuevo evento"""
        pass

    @abstractmethod
    def register_user_to_event(self, id_usuario: int, id_evento: int):
        """Registrar un usuario a un evento"""
        pass

    @abstractmethod
    def get_event_by_id(self, id_evento: int) -> Optional[Event]:
        """Obtener un evento por su ID"""
        pass

    @abstractmethod
    def get_events_by_user_id(self, id_usuario: int) -> List[Event]:
        """Obtener todos los eventos de un usuario"""
        pass

    @abstractmethod
    def get_activities_events(self, current_date: object, current_time: object) -> List[Event]:
        """Obtener todos los eventos vigentes"""
        pass
