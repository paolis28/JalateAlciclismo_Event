from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, time

import random
import string

def generate_clave():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

class Event(BaseModel):
    id_evento: Optional[int] = None
    id_usuario: Optional[int] = None
    clave: str = Field(default_factory=generate_clave)
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
    privado: Optional[int] = None


