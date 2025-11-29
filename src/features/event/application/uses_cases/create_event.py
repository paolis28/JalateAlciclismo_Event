import cloudinary
import cloudinary.uploader
from src.features.event.domain.port.Ievent_repository import EventRepositoryPort

cloudinary.config(
    cloud_name="url_perfil",
    api_key="782294236213671",
    api_secret="_Qd4Z_FD3Z_Lb897PAGptEP7Eds"
)

class CreateEventUseCase:
    def __init__(self, event_repository: EventRepositoryPort):
        self.repo = event_repository

    def execute(self, event_data, file=None):
        url_banner = None
        if file:
            upload_result = cloudinary.uploader.upload(
                file.file, folder="eventos", resource_type="image"
            )
            url_banner = upload_result.get("secure_url")
        event_data.url_banner = url_banner
        return self.repo.create_event(event_data)