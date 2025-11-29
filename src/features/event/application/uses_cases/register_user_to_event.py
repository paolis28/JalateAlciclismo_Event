from src.features.event.domain.port.Ievent_repository import EventRepositoryPort

class RegisterUserToEventUseCase:
    def __init__(self, event_repository: EventRepositoryPort):
        self.repo = event_repository

    def execute(self, id_usuario: int, id_evento: int):
        return self.repo.register_user_to_event(id_usuario, id_evento)