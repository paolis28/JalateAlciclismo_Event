from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import Optional
from src.features.event.domain.entities.event import Event
from src.features.event.application.uses_cases.create_event import CreateEventUseCase
from src.features.event.application.uses_cases.register_user_to_event import RegisterUserToEventUseCase
from src.features.event.dependency import (
    get_create_event_use_case_dependency,
)
from src.utils.jwt_handler import get_current_user_id  # Importar la función de autenticación

router = APIRouter(prefix="/event/v1", tags=["Events"])


@router.post("/create", status_code=201)
async def create_event(
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    cantidad_participantes: int = Form(0),
    origen_carrera: Optional[str] = Form(None),
    destino_fin_carrera: Optional[str] = Form(None),
    km: Optional[float] = Form(None),
    fecha_evento: Optional[str] = Form(None),  # Recibimos como string y pydantic/db lo manejarán, o convertimos si es necesario
    hora_evento: Optional[str] = Form(None),
    estatus: Optional[int] = Form(None),
    url_banner: Optional[str] = Form(None),
    use_case: CreateEventUseCase = Depends(get_create_event_use_case_dependency),
    current_user_id: int = Depends(get_current_user_id)  # Extraer el ID del usuario autenticado
):
    """Crear un nuevo evento"""
    try:
        event_data = Event(
            nombre=nombre,
            descripcion=descripcion,
            cantidad_participantes=cantidad_participantes,
            origen_carrera=origen_carrera,
            destino_fin_carrera=destino_fin_carrera,
            km=km,
            url_banner=None, # Se llena en el use case si hay archivo
            fecha_evento=fecha_evento,
            hora_evento=hora_evento,
            estatus=estatus,
            id_usuario=current_user_id  
        )
        result = use_case.execute(event_data, file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))