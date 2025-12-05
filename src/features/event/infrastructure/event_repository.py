from sqlalchemy import text
from src.features.db.db_config import engine
from src.features.event.domain.entities.event import Event
from src.features.event.domain.port.Ievent_repository import EventRepositoryPort
from typing import List, Optional

class EventRepository(EventRepositoryPort):
    
    def create_event(self, event_data: Event):
        """Crear un nuevo evento"""
        query = text("""
            INSERT INTO evento (id_usuario, clave, nombre, descripcion, cantidad_participantes, origen_carrera, destino_fin_carrera, km, url_banner,
             fecha_evento, hora_evento, estatus, privado)
            VALUES (:id_usuario, :clave, :nombre, :descripcion, :cantidad_participantes, :origen_carrera, :destino_fin_carrera, :km, :url_banner,
             :fecha_evento, :hora_evento, :estatus, :privado)
        """)
        with engine.connect() as conn:
            result = conn.execute(query, event_data.dict(exclude={'id_evento'}))
            conn.commit()
            return {"message": "Evento creado correctamente", "id_evento": result.lastrowid}


    def register_user_to_event(self, id_usuario: int, id_evento: int):
        """Registrar un usuario a un evento"""
        query = text("""
            INSERT INTO registered_user_to_event (id_usuario, id_evento)
            VALUES (:id_usuario, :id_evento)
        """)
        try:
            with engine.connect() as conn:
                conn.execute(query, {"id_usuario": id_usuario, "id_evento": id_evento})
                conn.commit()
                return {"message": "Usuario registrado al evento correctamente"}
        except Exception as e:
            # Manejar duplicados u otros errores
            if "Duplicate entry" in str(e):
                 return {"message": "El usuario ya está registrado en este evento", "error": True}
            raise e

    def get_event_by_id(self, id_evento: int) -> Optional[Event]:
        """Obtener un evento por su ID"""
        query = text("SELECT id_evento FROM evento WHERE id_evento = :id_evento")
        with engine.connect() as conn:
            result = conn.execute(query, {"id_evento": id_evento}).fetchone()
            if result:
                return Event(**result._mapping)
            return None
   
    def get_events_by_user_id(self, id_usuario: int) -> List[Event]:
        """Obtener todos los eventos de un usuario"""
        query = text("""
            SELECT 
                e.id_evento, e.id_usuario, e.clave, e.nombre, e.descripcion, e.cantidad_participantes, 
                e.origen_carrera, e.destino_fin_carrera, e.km, e.url_banner, e.fecha_evento, 
                CAST(e.hora_evento AS CHAR) as hora_evento, e.estatus, e.privado,
                COUNT(r.id_usuario) AS registered_users_count
            FROM evento e
            LEFT JOIN registered_user_to_event r ON e.id_evento = r.id_evento
            WHERE e.id_usuario = :id_usuario
            GROUP BY e.id_evento
        """)
        with engine.connect() as conn:
            result = conn.execute(query, {"id_usuario": id_usuario}).fetchall()
            return [Event(**row._mapping) for row in result]


    def get_activities_events(self, current_date: object, current_time: object) -> List[Event]:
        """Obtener todos los eventos vigentes (fecha >= hoy y hora > actual si es hoy)"""
        query = text("""
            SELECT 
                id_evento, id_usuario, clave, nombre, descripcion, cantidad_participantes, 
                origen_carrera, destino_fin_carrera, km, url_banner, fecha_evento, 
                CAST(hora_evento AS CHAR) as hora_evento, estatus, privado
            FROM evento 
            WHERE fecha_evento < :current_date 
            OR (fecha_evento = :current_date AND hora_evento < :current_time)
        """)
        with engine.connect() as conn:
            result = conn.execute(query, {
                "current_date": current_date,
                "current_time": current_time
            }).fetchall()
            return [Event(**row._mapping) for row in result]
