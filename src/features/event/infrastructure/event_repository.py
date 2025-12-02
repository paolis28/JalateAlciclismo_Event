from sqlalchemy import text
from src.features.db.db_config import engine
from src.features.event.domain.entities.event import Event
from src.features.event.domain.port.Ievent_repository import EventRepositoryPort
from typing import List, Optional

class EventRepository(EventRepositoryPort):
    
    def create_event(self, event_data: Event):
        """Crear un nuevo evento"""
        query = text("""
            INSERT INTO evento (id_usuario, nombre, descripcion, cantidad_participantes, origen_carrera, destino_fin_carrera, km, url_banner,
             fecha_evento, hora_evento, estatus)
            VALUES (:id_usuario, :nombre, :descripcion, :cantidad_participantes, :origen_carrera, :destino_fin_carrera, :km, :url_banner,
             :fecha_evento, :hora_evento, :estatus)
        """)
        with engine.connect() as conn:
            result = conn.execute(query, event_data.dict(exclude={'id_evento'}))
            conn.commit()
            return {"message": "Evento creado correctamente", "id_evento": result.lastrowid}
