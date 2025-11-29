from abc import ABC, abstractmethod
from typing import List, Optional
from src.features.event.domain.entities.event import Event

class EventRepositoryPort(ABC):
    @abstractmethod
    def create_event(self, event_data: Event):
        """Crear un nuevo evento"""
        pass
