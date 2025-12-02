from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class Event(BaseModel):
    id_evento: Optional[int] = None
    id_usuario: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    cantidad_participantes: int = 0
    origen_carrera: Optional[str] = None
    destino_fin_carrera: Optional[str] = None
    km: Optional[float] = None
    url_banner: Optional[str] = None
    fecha_evento: Optional[date] = None
    hora_evento: Optional[time] = None
    estatus: Optional[int] = None
