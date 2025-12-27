# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a full-stack LLM chat application consisting of:
- **Backend**: Python FastAPI REST API (`backend/`)
- **Frontend**: Next.js 15 web application (`frontend/`)

Each directory has its own `CLAUDE.md` file with detailed guidance:
- See `backend/CLAUDE.md` for backend architecture, commands, and development workflow
- See `frontend/CLAUDE.md` for frontend architecture, commands, and component patterns

## Repository Structure

```
llm-chat/
├── backend/              # Python FastAPI backend
│   ├── CLAUDE.md         # Backend-specific guidance
│   ├── llm_chat_backend/ # Source code
│   ├── docs/             # Architecture documentation
│   ├── pyproject.toml    # Python dependencies (uv)
│   └── .env.local        # Environment configuration
├── frontend/             # Next.js 15 frontend
│   ├── CLAUDE.md         # Frontend-specific guidance
│   ├── app/              # Next.js App Router pages
│   ├── components/       # React components
│   ├── package.json      # Node dependencies (pnpm)
│   └── tailwind.config.js
└── docs/                 # Project documentation
```

## Quick Start

### Running the Full Stack

**Terminal 1 - Backend:**
```bash
cd backend
uv sync
uv run python -m llm_chat_backend.presentation.routes.main
# Server starts at http://127.0.0.1:8000
# API docs at http://127.0.0.1:8000/docs
```

**Terminal 2 - Frontend:**
```bash
cd frontend
pnpm install
pnpm dev
# App starts at http://localhost:3000
```

## Technology Stack

### Backend
- **Language**: Python 3.13
- **Package Manager**: uv
- **Framework**: FastAPI
- **Database**: SQLite (dev), PostgreSQL (production planned)
- **Architecture**: Clean Architecture + Domain-Driven Design

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Package Manager**: pnpm
- **UI Library**: HeroUI v2
- **Styling**: Tailwind CSS v4
- **Language**: TypeScript 5.6

## API Integration

The frontend communicates with the backend via REST API:
- **Backend API**: http://127.0.0.1:8000
- **Frontend Dev**: http://localhost:3000

### Example API Endpoints

```
GET    /chats?user_id={id}              # List user's chats
POST   /chats                            # Create new chat
GET    /chats/{chat_id}?user_id={id}    # Get chat with messages
PATCH  /chats/{chat_id}                 # Update chat title
DELETE /chats/{chat_id}?user_id={id}    # Delete chat
POST   /chats/{chat_id}/messages        # Send message (streaming)
```

See backend API docs at http://127.0.0.1:8000/docs for complete API reference.

## Key Architectural Principles

### Backend (Clean Architecture)

The backend follows strict layered architecture:
1. **Domain** → Business entities and interfaces (no dependencies)
2. **Application** → Use cases and orchestration
3. **Infrastructure** → Database, external APIs
4. **Presentation** → HTTP routes, UI

**Critical Rule**: Dependencies point inward. Domain layer has no knowledge of outer layers.

### Frontend (Component-Based)

The frontend follows Next.js 15 conventions:
- **Server Components** by default (better performance)
- **Client Components** for interactivity (`"use client"`)
- **App Router** for file-based routing

## Development Workflow

When adding new features:

1. **Backend First** (if API changes needed):
   - Define domain entities and repository interfaces
   - Implement use cases in application layer
   - Add repository implementations
   - Create FastAPI routes
   - See `backend/CLAUDE.md` for detailed workflow

2. **Frontend** (consume backend API):
   - Create/update components
   - Integrate with backend API
   - Handle loading and error states
   - See `frontend/CLAUDE.md` for patterns

## Environment Configuration

### Backend Environment Variables

Create `backend/.env.local`:
```bash
SQLITE_DB_PATH=".data/chat.db"
SQLITE_ECHO=false
```

### Frontend Environment Variables

Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Documentation

- `backend/docs/1_functional_requirements.md` - Feature requirements
- `backend/docs/2_development_guide.md` - Detailed architecture guide
- `backend/CLAUDE.md` - Backend development guidance
- `frontend/CLAUDE.md` - Frontend development guidance
