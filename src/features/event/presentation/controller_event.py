from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import Optional
from src.features.event.domain.entities.event import Event
from src.features.event.application.uses_cases.create_event import CreateEventUseCase
from src.features.event.application.uses_cases.register_user_to_event import RegisterUserToEventUseCase
from src.features.event.dependency import (
    get_create_event_use_case_dependency,
)

router = APIRouter(prefix="/event/v1", tags=["Events"])


@router.post("/create", status_code=201)
async def create_event(
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    cantidad_participantes_dis: int = Form(0),
    origen_carrera: Optional[str] = Form(None),
    km: Optional[float] = Form(None),
    file: Optional[UploadFile] = File(None),
    use_case: CreateEventUseCase = Depends(get_create_event_use_case_dependency)
):
    """Crear un nuevo evento"""
    try:
        event_data = Event(
            nombre=nombre,
            descripcion=descripcion,
            cantidad_participantes_dis=cantidad_participantes_dis,
            origen_carrera=origen_carrera,
            km=km
        )
        result = use_case.execute(event_data, file)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


