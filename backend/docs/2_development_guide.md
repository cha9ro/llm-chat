# Development Guide

This document defines the architectural standards, technical stack, and development guidelines for the `llm-chat-backend` project. It is intended to guide AI agents in generating code that aligns with **Domain-Driven Design (DDD)** principles.

## 1. Architectural Overview

The project follows a **Clean Architecture** style.

### Core Principles

- **Dependency Rule**: Dependencies must point **inwards**. Inner layers (Domain) must not know about outer layers (Infrastructure, Presentation).
- **Dependency Injection (DI)**: Use `injector` to decouple components. Interfaces are defined in inner layers; implementations are injected from outer layers.
- **Separation of Concerns**: Isolate business logic from technical details (DB, API, UI).

## 2. Layer Definitions & Responsibilities

### Domain Layer (`llm_chat_backend/domain`)

- **Role**: The heart of the software. Encapsulates enterprise business rules and state.
- **Structure**: Organized by **Domain Modules** (e.g., `chat`, `user`).
- **Components**:
  - `model.py`: Entities and Value Objects.
  - `repository.py`: Repository Interfaces.
- **Rules**:
  - **Pure Python**: Minimal external dependencies.
  - **No Infrastructure**: No SQL, no HTTP calls.
  - **Pydantic Usage**: Allowed for validation and Value Objects.

### Application Layer (`llm_chat_backend/application`)

- **Role**: Orchestrates Domain objects to fulfill specific user use cases.
- **Components**: Application Services (e.g., `inference.py`).
- **Rules**:
  - **Orchestration**: Delegates to Domain entities/services.
  - **Transaction Management**: Handles database transactions.
  - **Input/Output**: Accepts primitives or DTOs, returns DTOs.

### Infrastructure Layer (`llm_chat_backend/infra`)

- **Role**: Provides technical implementations for interfaces defined in the Domain/Application layers.
- **Components**: Repository Implementations (SQLAlchemy), External API Clients, DB Adapters.
- **Rules**:
  - **Adapters**: Converts Domain Entities to ORM Models and vice versa.

### Presentation Layer (`llm_chat_backend/presentation`)

- **Role**: Interface for the outside world (API & UI).
- **Components**:
  - `routes/`: FastAPI Routes (Controllers).
  - `ui/`: Streamlit UI scripts.
- **Rules**:
  - **Thin Layer**: Handles request parsing and response formatting.
  - **Delegation**: Calls Application Services.

## 3. Technical Stack

### Core

- **Language**: Python 3.13+
- **DI Container**: `injector`
- **Type Checking**: `pydantic`

### Data Persistence (Infrastructure)

- **ORM**: **SQLAlchemy** (Recommended for implementing DDD Repositories)
- **Migrations**: **Alembic** (DDL Management)
- **Database**:
  - **Production**: `PostgreSQL`
  - **Dev/Test**: `SQLite` (via `sqlite3` driver)

### Web API (Presentation)

- **Framework**: `fastapi`
- **API Style**: RESTful

### User Interface (Presentation)

- **PoC/Internal**: `streamlit`

## 4. Implementation Guidelines for Agents

1.  **Development Flow**: Start from the **Domain** (Entities/Interfaces) -> **Application** (Use Cases) -> **Infrastructure** (Persistence) -> **Presentation** (API).
2.  **Repositories**: Always define the interface in `domain/{module}/repository.py` and implement in `infra`.
3.  **DTOs** : Use Pydantic models for DTOs in the Application layer to decouple the API contract from the Domain model.
