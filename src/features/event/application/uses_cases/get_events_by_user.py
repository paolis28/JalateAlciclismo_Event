from typing import List
from src.features.event.domain.port.Ievent_repository import EventRepositoryPort
from src.features.event.domain.entities.event import Event

class GetEventsByUserUseCase:
    def __init__(self, event_repository: EventRepositoryPort):
        self.repo = event_repository

    def execute(self, id_usuario: int) -> List[Event]:
        return self.repo.get_events_by_user_id(id_usuario)
