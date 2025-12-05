from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import Optional
from src.features.event.domain.entities.event import Event
from src.features.event.application.uses_cases.create_event import CreateEventUseCase
from src.features.event.application.uses_cases.register_user_to_event import RegisterUserToEventUseCase
from src.features.event.dependency import (
    get_create_event_use_case_dependency,
    get_register_user_to_event_use_case_dependency,
    get_get_events_by_user_id_use_case_dependency,
)
from src.features.event.application.uses_cases.get_events_by_user import GetEventsByUserUseCase
from src.utils.jwt_handler import get_current_user_id
from src.services.cloudinary_service import CloudinaryService

router = APIRouter(prefix="/event/v1", tags=["Events"])


@router.post("/create", status_code=201)
async def create_event(
    nombre: str = Form(...),
    descripcion: Optional[str] = Form(None),
    cantidad_participantes: int = Form(0),
    origen_carrera: Optional[str] = Form(None),
    destino_fin_carrera: Optional[str] = Form(None),
    km: Optional[float] = Form(None),
    fecha_evento: Optional[str] = Form(None),
    hora_evento: Optional[str] = Form(None),
    estatus: Optional[int] = Form(None),
    file_banner: Optional[UploadFile] = File(None),
    privado: Optional[int] = Form(None),
    use_case: CreateEventUseCase = Depends(get_create_event_use_case_dependency),
    current_user_id: int = Depends(get_current_user_id)
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
            url_banner="https://www.escapadarural.com/blog/wp-content/uploads/AdobeStock_346468147-scaled.jpeg",
            fecha_evento=fecha_evento,
            hora_evento=hora_evento,
            estatus=estatus,
            id_usuario=current_user_id,
            privado=privado
        )
        
        if file_banner:
            print("Subiendo banner")
            try:
                cloudinary_service = CloudinaryService()
                event_data.url_banner = cloudinary_service.upload_image(file_banner)
                print("Banner subido exitosamente")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error al tratar de subir el banner: {e}")
        
        result = use_case.execute(event_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{id_evento}/register", status_code=201)
async def register_user_to_event(
    id_evento: int,
    use_case: RegisterUserToEventUseCase = Depends(get_register_user_to_event_use_case_dependency),
    current_user_id: int = Depends(get_current_user_id)
):
    """Registrar un usuario a un evento"""
    try:
        result = use_case.execute(id_usuario=current_user_id, id_evento=id_evento)
        if result.get("error"):
             raise HTTPException(status_code=400, detail=result.get("message"))
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by_user_id", status_code=200)
async def get_events_by_user_id(
    use_case: GetEventsByUserUseCase = Depends(get_get_events_by_user_id_use_case_dependency),
    current_user_id: int = Depends(get_current_user_id)
):
    """Obtener todos los eventos de un usuario"""
    try:
        result = use_case.execute(id_usuario=current_user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))