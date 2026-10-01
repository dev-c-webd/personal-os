# Personal OS — Roadmap

This document is the master roadmap for Personal OS.

It records:
- the original long-term engineering roadmap
- the current implementation phase
- completed phases
- deferred work
- major future capabilities
- the distinction between what is implemented now and what is intentionally left for later

The roadmap is intentionally long-term. Not every idea listed here should be implemented immediately.

---

## Project Direction

Personal OS is being built as a long-term, customizable personal environment rather than a simple notes or task application.

The goal is to learn and implement the full modern software engineering lifecycle through one real application:

idea → architecture → backend → database → authentication → APIs → testing → containers → cloud → CI/CD → observability → reliability → infrastructure → AI → agents → production systems.

The application should remain useful as the architecture becomes more advanced.

---

# Engineering Roadmap

## 1. Backend Fundamentals ✅

Completed foundation for:
- Python backend structure
- application modules
- dependency management
- environment configuration
- basic backend architecture

---

## 2. FastAPI ✅

Completed foundation for:
- FastAPI application
- routers
- path parameters
- request bodies
- response schemas
- dependency injection
- API versioning
- authentication dependencies

Current API convention:

`/api/v1/...`

---

## 3. PostgreSQL + SQLAlchemy + Alembic ✅

Completed foundation for:
- PostgreSQL
- SQLAlchemy ORM
- SQLAlchemy models
- database sessions
- Alembic migrations
- migration verification
- UUID identifiers
- foreign keys
- composite foreign keys
- recursive PostgreSQL queries where required

Database design principle:

Use relational structure for important domain relationships.

Use JSONB where flexibility is actually required.

Do not turn the whole application into an unstructured JSON database.

---

## 4. Authentication ✅

Implemented:
- user registration
- login
- password hashing
- JWT authentication
- current-user dependency
- authenticated user endpoints

Authorization foundation:
- workspace membership
- workspace-scoped access checks

Authentication and authorization remain separate concepts.

---

## 5. Workspace + Hierarchical Data Model ✅

Implemented:
- User
- Workspace
- WorkspaceMember
- universal Page representation using the existing `nodes` table
- UUID identifiers
- arbitrary Page hierarchy
- workspace-scoped parent relationships
- sibling ordering
- Page creation/read/update/delete
- Page movement
- cycle prevention
- recursive subtree deletion

Important architectural decision:

Pages are universal containers.

A Page is NOT permanently classified as:
- folder
- note
- task
- goal
- file

Instead, those concepts can later be represented by actual domain objects, components, views, or combinations of these.

---

# 6. Personal OS Resources ← CURRENT

This is the main product architecture phase.

---

## 6.1 Core Product Architecture ✅

Established conceptual architecture:

```text
Workspace
   └── Page
       ├── Page Settings
       └── Component Placements
            └── Components
                 └── Data / Entity Bindings