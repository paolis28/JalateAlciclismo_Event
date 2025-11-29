from pydantic import BaseModel
from typing import Optional

class Event(BaseModel):
    id_evento: Optional[int] = None
    nombre: str
    descripcion: Optional[str] = None
    cantidad_participantes_dis: int = 0
    origen_carrera: Optional[str] = None
    km: Optional[float] = None
    url_banner: Optional[str] = None
    usuario_id: Optional[int] = None
