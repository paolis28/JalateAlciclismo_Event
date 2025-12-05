from typing import List
from src.features.event.domain.entities.event import Event
from src.features.event.infrastructure.event_repository import EventRepository
from datetime import date, time

class GetActivitiesEventsUseCase:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    def execute(self, current_date: date, current_time: time) -> List[Event]:
        return self.repository.get_activities_events(current_date, current_time)
