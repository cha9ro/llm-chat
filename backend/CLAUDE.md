# CLAUDE.md - Backend

This file provides guidance to Claude Code when working with the backend of this repository.

## Technology Stack

- **Language**: Python 3.13
- **Package Manager**: uv
- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy-based)
- **Database**: SQLite (dev), PostgreSQL (production)
- **DI Container**: injector
- **Type Checking**: pyright
- **Linting/Formatting**: ruff

## Development Commands

All commands should be run from the `backend/` directory:

```bash
# Install dependencies
uv sync

# Run development server (http://127.0.0.1:8000)
uv run python -m llm_chat_backend.presentation.routes.main

# API documentation available at:
# - http://127.0.0.1:8000/docs (Swagger UI)
# - http://127.0.0.1:8000/redoc (ReDoc)

# Type checking
uv run pyright

# Linting
uv run ruff check

# Formatting
uv run ruff format

# Run tests
uv run pytest
```

## Architecture

This backend strictly follows **Clean Architecture** and **Domain-Driven Design (DDD)** principles.

### Core Principle: The Dependency Rule

**Dependencies must point inwards** toward the domain layer. Inner layers (domain) must NEVER depend on outer layers (infrastructure, presentation).

### Layer Structure

```
llm_chat_backend/
├── domain/              # Business logic and contracts
│   ├── model/           # Domain entities (Chat, Message, User, etc.)
│   └── repository/      # Repository interfaces (IChatRepository, etc.)
├── application/         # Use cases and orchestration
│   ├── chat.py          # ChatUsecase
│   └── response.py      # ResponseUsecase
├── infra/               # Technical implementations
│   ├── database/        # Database configuration (SQLite/PostgreSQL)
│   ├── repository/      # Repository implementations
│   ├── agent/           # LLM agent implementations
│   └── client/          # External API clients
└── presentation/        # External interfaces
    ├── routes/          # FastAPI route handlers
    └── ui/              # Streamlit UI (if used)
```

### Layer Responsibilities

#### 1. Domain Layer (`domain/`)

**Purpose**: The heart of the application. Contains business rules and domain logic.

**Rules**:
- Pure Python with minimal external dependencies
- Defines entities as Pydantic models
- Defines repository interfaces as Abstract Base Classes
- NO infrastructure concerns (no SQL, HTTP, file I/O, etc.)
- NO dependencies on outer layers

**Examples**:
- Entities: `Chat`, `Message`, `User`, `Content`
- Interfaces: `IChatRepository`, `IMessageRepository`

#### 2. Application Layer (`application/`)

**Purpose**: Orchestrates domain objects to fulfill specific use cases.

**Rules**:
- Contains application-specific business logic
- Orchestrates domain entities and services
- Handles transaction management
- Accepts primitives or DTOs as input, returns DTOs
- Depends on domain layer interfaces, not implementations

**Examples**:
- `ChatUsecase.create_chat()` - Creates a new chat session
- `ChatUsecase.delete_chat()` - Validates ownership and deletes
- `ResponseUsecase` - Generates LLM responses

#### 3. Infrastructure Layer (`infra/`)

**Purpose**: Provides technical implementations for interfaces defined in domain/application layers.

**Rules**:
- Implements repository interfaces from domain layer
- Handles database persistence (SQLModel/SQLAlchemy)
- Manages external API clients
- Converts between domain entities and database models

**Examples**:
- `ChatRepository` implements `IChatRepository`
- `SQLiteConnection` provides database session management
- LLM client implementations

#### 4. Presentation Layer (`presentation/`)

**Purpose**: Interface with the outside world (HTTP API, UI).

**Rules**:
- Thin layer for request/response handling
- Delegates all logic to application layer
- Handles HTTP-specific concerns (status codes, error formatting)
- Defines request/response DTOs separate from domain models

**Examples**:
- FastAPI routes in `routes/chat.py`
- Request models: `ChatCreateRequest`, `ChatTitleUpdateRequest`
- Response models: Domain entities serialized as JSON

## Dependency Injection

The project uses two DI systems working together:

### 1. Injector (Application DI)

Configured in `dependencies.py`:

```python
class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # Bind interfaces to implementations
        binder.bind(IChatRepository, to=ChatRepository, scope=singleton)
        binder.bind(ChatUsecase, to=ChatUsecase, scope=singleton)
```

Usage in application/domain layers:

```python
from injector import inject

class ChatUsecase:
    @inject
    def __init__(self, chat_repository: IChatRepository) -> None:
        self._chat_repository = chat_repository
```

### 2. FastAPI Depends (Presentation DI)

Usage in routes to integrate with injector:

```python
from fastapi import Depends
from injector import Injector

def get_chat_usecase(
    injector: Annotated[Injector, Depends(get_injector)]
) -> ChatUsecase:
    return injector.get(ChatUsecase)

@router.post("/chats")
async def create_chat(
    usecase: Annotated[ChatUsecase, Depends(get_chat_usecase)],
    request: ChatCreateRequest,
) -> Chat:
    return usecase.create_chat(user_id=request.user_id, title=request.title)
```

**Important**: Routes use FastAPI's `Depends` to get the injector, then use injector to get use cases.

## Database

### Configuration

- **ORM**: SQLModel (combines SQLAlchemy and Pydantic)
- **Dev/Test**: SQLite
- **Production**: PostgreSQL (planned)
- **Connection Management**: `SQLiteConnection` class in `infra/database/sqlite.py`

### Environment Variables

Set in `.env.{APP_PROFILE}` (e.g., `.env.local`):

```bash
SQLITE_DB_PATH=".data/chat.db"
SQLITE_ECHO=false
```

Profile selection:
```bash
export APP_PROFILE=local  # Loads .env.local (default)
export APP_PROFILE=prod   # Would load .env.prod
```

### Database Initialization

SQLModel tables are created automatically via `SQLiteConnection.create_all()`. This is typically called at application startup.

### Session Management

Always use the context manager pattern:

```python
from llm_chat_backend.infra.database.sqlite import SQLiteConnection

class ChatRepository:
    def __init__(self, connection: SQLiteConnection):
        self._connection = connection

    def create_chat(self, chat: Chat) -> Chat:
        with self._connection.session() as session:
            # ... database operations
            session.commit()
```

## Development Workflow

When implementing new features, follow this order:

### 1. Start with Domain Layer

Define entities and interfaces:

```python
# domain/model/feature.py
class Feature(BaseModel):
    id: str
    name: str

# domain/repository/feature.py
class IFeatureRepository(ABC):
    @abstractmethod
    def create_feature(self, feature: Feature) -> Feature:
        pass
```

### 2. Create Application Use Cases

```python
# application/feature.py
class FeatureUsecase:
    @inject
    def __init__(self, repository: IFeatureRepository) -> None:
        self._repository = repository

    def create_feature(self, name: str) -> Feature:
        feature = Feature(id=str(uuid4()), name=name)
        return self._repository.create_feature(feature)
```

### 3. Implement Infrastructure

```python
# infra/repository/feature.py
class FeatureRepository(IFeatureRepository):
    def create_feature(self, feature: Feature) -> Feature:
        # Implementation with SQLModel
        pass
```

### 4. Add Presentation Layer

```python
# presentation/routes/feature.py
class FeatureCreateRequest(BaseModel):
    name: str

@router.post("/features")
async def create_feature(
    usecase: Annotated[FeatureUsecase, Depends(get_feature_usecase)],
    request: FeatureCreateRequest,
) -> Feature:
    return usecase.create_feature(name=request.name)
```

### 5. Register Dependencies

```python
# dependencies.py
class AppModule(Module):
    def configure(self, binder: Binder) -> None:
        # Add new bindings
        binder.bind(IFeatureRepository, to=FeatureRepository, scope=singleton)
        binder.bind(FeatureUsecase, to=FeatureUsecase, scope=singleton)
```

## Critical Guidelines

- **Repository interfaces** must be defined in `domain/repository/`, never in `infra/`
- **Domain entities** must not depend on database models
- **Use cases** should only depend on domain interfaces, not concrete implementations
- **All database operations** must go through repository implementations
- **Business logic** belongs in domain/application layers, NOT in routes or repositories
- **Request/Response models** in routes should be separate from domain models
- Use `@inject` decorator for constructor dependency injection
- Follow existing session management patterns with SQLModel
- Naming convention: Repository interfaces start with `I` (e.g., `IChatRepository`)
