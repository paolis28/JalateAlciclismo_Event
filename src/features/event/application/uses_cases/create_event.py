
from src.features.event.domain.port.Ievent_repository import EventRepositoryPort

class CreateEventUseCase:
    def __init__(self, event_repository: EventRepositoryPort):
        self.repo = event_repository

    def execute(self, event_data):
        return self.repo.create_event(event_data)
    