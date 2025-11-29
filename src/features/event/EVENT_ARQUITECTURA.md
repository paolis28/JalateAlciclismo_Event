# 🏗️ Arquitectura Event Feature - Inyección de Dependencias

## Estructura de Directorios

```
src/features/event/
├── domain/
│   ├── entities/
│   │   └── event.py ............................ [NO CAMBIA]
│   └── port/
│       └── Ievent_repository.py ................ [NO CAMBIA]
│
├── application/
│   └── uses_cases/
│       ├── create_event.py ..................... [ACTUALIZAR]
│       ├── get_event.py ........................ [ACTUALIZAR]
│       ├── update_event.py ..................... [ACTUALIZAR]
│       ├── delete_event.py ..................... [ACTUALIZAR]
│       ├── register_user_to_event.py ........... [ACTUALIZAR]
│       └── get_event_participants.py ........... [ACTUALIZAR]
│
├── infrastructure/
│   └── event_repository.py ..................... [NO CAMBIA]
│
├── presentation/
│   └── controller_event.py ..................... [ACTUALIZAR]
│
└── dependency_injection.py ..................... [NUEVO]
```

## Flujo de Inyección de Dependencias

```
[POST /event/create]
        │
        ▼
┌───────────────────────────────────────┐
│  controller_event.py                  │
│  @router.post("/create")              │
│  async def create_event(              │
│    use_case = Depends(                │
│      get_create_event_use_case...     │
│    )                                  │
│  )                                    │
└────────────┬──────────────────────────┘
             │
             ▼
┌───────────────────────────────────────┐
│  dependency_injection.py              │
│                                       │
│  EventDependencyContainer             │
│    .get_create_event_use_case()      │
│         │                             │
│         └─► get_event_repository()   │
└────────────┬──────────────────────────┘
             │
             ▼
┌───────────────────────────────────────┐
│  CreateEventUseCase(                  │
│    event_repository=EventRepository() │
│  )                                    │
└────────────┬──────────────────────────┘
             │
             ▼
┌───────────────────────────────────────┐
│  EventRepository                      │
│    implements EventRepositoryPort     │
│         │                             │
│         ▼                             │
│    [DATABASE]                         │
└───────────────────────────────────────┘
```

## Arquitectura Completa

```
┌─────────────────────────────────────────────────────┐
│              PRESENTATION LAYER                      │
│  ┌───────────────────────────────────────────────┐  │
│  │        controller_event.py                    │  │
│  │                                               │  │
│  │  POST   /event/create                        │  │
│  │  GET    /event/get_all                       │  │
│  │  GET    /event/{id}                          │  │
│  │  PUT    /event/{id}                          │  │
│  │  DELETE /event/{id}                          │  │
│  │  POST   /event/{id}/register/{user_id}      │  │
│  │  GET    /event/{id}/participants             │  │
│  │                                               │  │
│  │  Todos usan: Depends(get_xxx_use_case...)   │  │
│  └────────────────┬──────────────────────────────┘  │
└────────────────────┼────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│         DEPENDENCY INJECTION LAYER                   │
│  ┌───────────────────────────────────────────────┐  │
│  │      dependency_injection.py                  │  │
│  │                                               │  │
│  │  EventDependencyContainer:                   │  │
│  │    - get_event_repository()                  │  │
│  │    - get_create_event_use_case()            │  │
│  │    - get_get_event_use_case()               │  │
│  │    - get_get_all_events_use_case()          │  │
│  │    - get_update_event_use_case()            │  │
│  │    - get_delete_event_use_case()            │  │
│  │    - get_register_user_to_event_use_case()  │  │
│  │    - get_get_event_participants_use_case()  │  │
│  └────────────────┬──────────────────────────────┘  │
└────────────────────┼────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│              APPLICATION LAYER                       │
│  ┌──────────────────┐  ┌──────────────────────┐    │
│  │ CreateEventUseCase│  │GetEventUseCase       │    │
│  │ UpdateEventUseCase│  │GetAllEventsUseCase   │    │
│  │ DeleteEventUseCase│  │RegisterUserToEvent   │    │
│  │                   │  │GetEventParticipants  │    │
│  │                   │  │                      │    │
│  │ __init__(         │  │__init__(             │    │
│  │   event_repository│  │  event_repository    │    │
│  │ )                 │  │)                     │    │
│  └────────┬──────────┘  └────────┬─────────────┘    │
└───────────┼──────────────────────┼──────────────────┘
            │                      │
            └──────────┬───────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                 DOMAIN LAYER                         │
│  ┌───────────────────────────────────────────────┐  │
│  │     Ievent_repository.py (PORT)               │  │
│  │                                               │  │
│  │  class EventRepositoryPort(ABC):             │  │
│  │    @abstractmethod                           │  │
│  │    def create_event(...)                     │  │
│  │    def get_all_events(...)                   │  │
│  │    def get_event_by_id(...)                  │  │
│  │    def update_event(...)                     │  │
│  │    def delete_event(...)                     │  │
│  │    def register_user_to_event(...)           │  │
│  │    def get_event_participants(...)           │  │
│  │    def unregister_user_from_event(...)       │  │
│  └────────────────┬──────────────────────────────┘  │
└────────────────────┼────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│           INFRASTRUCTURE LAYER                       │
│  ┌───────────────────────────────────────────────┐  │
│  │     event_repository.py (ADAPTER)             │  │
│  │                                               │  │
│  │  class EventRepository(EventRepositoryPort): │  │
│  │    def create_event(...)                     │  │
│  │    def get_all_events(...)                   │  │
│  │    def get_event_by_id(...)                  │  │
│  │    def update_event(...)                     │  │
│  │    def delete_event(...)                     │  │
│  │    def register_user_to_event(...)           │  │
│  │    def get_event_participants(...)           │  │
│  └────────────────┬──────────────────────────────┘  │
└────────────────────┼────────────────────────────────┘
                     │
                     ▼
              ┌──────────────┐
              │   DATABASE   │
              │   (MySQL)    │
              └──────────────┘
```

## Comparación ANTES vs DESPUÉS

### ANTES ❌
```python
# create_event.py
class CreateEventUseCase:
    def __init__(self):
        self.repo = EventRepository()  # Dependencia dura

# get_event.py  
class GetAllEventsUseCase:
    def __init__(self):
        self.repo = EventRepository()  # Dependencia dura

# controller_event.py
@router.post("/create")
async def create_event(...):
    use_case = CreateEventUseCase()  # Creación manual
    result = use_case.execute(event_data, file)
```

### DESPUÉS ✅
```python
# create_event.py
class CreateEventUseCase:
    def __init__(self, event_repository: EventRepositoryPort):
        self.repo = event_repository  # ✅ Inyección

# get_event.py
class GetAllEventsUseCase:
    def __init__(self, event_repository: EventRepositoryPort):
        self.repo = event_repository  # ✅ Inyección

# controller_event.py
@router.post("/create")
async def create_event(
    ...,
    use_case: CreateEventUseCase = Depends(get_create_event_use_case_dependency)
):
    result = use_case.execute(event_data, file)
```

## Mapa de Endpoints y Dependencias

```
POST   /event/create
       └─► get_create_event_use_case_dependency()
           └─► CreateEventUseCase(EventRepository)

GET    /event/get_all
       └─► get_get_all_events_use_case_dependency()
           └─► GetAllEventsUseCase(EventRepository)

GET    /event/{id_evento}
       └─► get_get_event_use_case_dependency()
           └─► GetEventUseCase(EventRepository)

PUT    /event/{id_evento}
       └─► get_update_event_use_case_dependency()
           └─► UpdateEventUseCase(EventRepository)

DELETE /event/{id_evento}
       └─► get_delete_event_use_case_dependency()
           └─► DeleteEventUseCase(EventRepository)

POST   /event/{id_evento}/register/{id_usuario}
       └─► get_register_user_to_event_use_case_dependency()
           └─► RegisterUserToEventUseCase(EventRepository)

GET    /event/{id_evento}/participants
       └─► get_get_event_participants_use_case_dependency()
           └─► GetEventParticipantsUseCase(EventRepository)
```

## Ciclo de Vida del Container

```
┌────────────────────────────────────────┐
│   Inicio de la Aplicación              │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│ EventDependencyContainer se crea       │
│ (Singleton - una sola vez)             │
│                                        │
│ _event_repository = None               │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│ Primera llamada a cualquier endpoint:  │
│                                        │
│ 1. FastAPI detecta Depends()           │
│ 2. Llama a get_xxx_use_case_...()     │
│ 3. Container verifica _event_repository│
│    - Si es None → Crea EventRepository │
│    - Si existe → Usa el existente      │
│ 4. Crea UseCase con repo inyectado    │
└──────────────┬─────────────────────────┘
               │
               ▼
┌────────────────────────────────────────┐
│ Llamadas subsecuentes:                 │
│                                        │
│ - Reutiliza el mismo EventRepository   │
│ - Crea nuevas instancias de UseCases  │
│ - Mantiene eficiencia y consistencia  │
└────────────────────────────────────────┘
```

## Checklist de Implementación

```
□ Crear dependency_injection.py en src/features/event/

□ Actualizar casos de uso:
  □ create_event.py
  □ get_event.py
  □ update_event.py
  □ delete_event.py
  □ register_user_to_event.py
  □ get_event_participants.py

□ Actualizar controller:
  □ controller_event.py

□ Probar endpoints:
  □ POST   /event/create
  □ GET    /event/get_all
  □ GET    /event/{id}
  □ PUT    /event/{id}
  □ DELETE /event/{id}
  □ POST   /event/{id}/register/{user_id}
  □ GET    /event/{id}/participants
```
