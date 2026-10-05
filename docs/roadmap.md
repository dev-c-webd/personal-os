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

Core principles established:

universal Pages
configurable Page appearance
configurable Page layout
configurable Page behavior
reusable Components
separate Component and Placement concepts
reusable underlying data
multiple presentations of the same underlying data
extensible composition system
configuration-driven UI
future AI-driven UI construction
6.2 Universal Page Implementation ✅

Completed:

removed fixed Node type
removed type from API schemas
removed type from services
removed type from router usage
migrated database
tested Page CRUD behavior
tested Page movement
tested hierarchy protection
tested recursive deletion

Current database representation:

nodes

Conceptually referred to as:

Page

6.3 Page Customization ✅

Implemented:

page_settings

Page settings contain:

appearance
layout_config
behavior_config

The settings are stored separately from the Page itself.

Current behavior:

settings can be created on first access
settings can be retrieved
individual configuration sections can be updated
workspace membership is enforced
settings belong to a Page
settings are deleted with their Page

Why separate settings from the Page:

Avoid continuously expanding the Page table with appearance and behavior fields.

Flexible configuration belongs in JSONB while the Page's core identity remains relational.

6.4 Component System ← CURRENT

Components are intended to become the foundation for customizable UI.

6.4.1 Component models + database ✅

Implemented:

components

and

component_placements

A Component represents the reusable thing.

A Placement represents where and how that Component appears.

This allows the same Component/data to have multiple presentations.

Example:

Task
 └── Component
      ├── Placement on Dashboard
      │     └── large card
      │
      └── Placement on Today page
            └── compact row

Database protections include workspace-aware composite foreign keys.

6.4.2 Component schemas ✅

Implemented:

ComponentCreate
ComponentUpdate
ComponentResponse
ComponentPlacementCreate
ComponentPlacementUpdate
ComponentPlacementResponse

Flexible configuration is represented with JSON-compatible structures.

6.4.3 Component service ✅ (local, pending checkpoint)

Implemented locally:

create component
list components
get component
update component
delete component

Service methods are workspace-scoped.

The service has been import-tested.

This phase still needs the normal repository checkpoint before being considered fully synchronized with GitHub.

# 6.4 Component System ✅

The Component System foundation is implemented and API-tested.

---

## 6.4.1 Component models + database ✅

Implemented:

- `components`
- `component_placements`
- UUID identifiers
- workspace ownership
- workspace-aware composite foreign keys
- cascade relationships
- flexible JSONB configuration

---

## 6.4.2 Component schemas ✅

Implemented:

- `ComponentCreate`
- `ComponentUpdate`
- `ComponentResponse`
- `ComponentPlacementCreate`
- `ComponentPlacementUpdate`
- `ComponentPlacementResponse`

---

## 6.4.3 Component service ✅

Implemented:

- create Component
- list Components
- retrieve Component
- update Component
- delete Component

Workspace scoping is enforced by the service.

PATCH behavior correctly distinguishes omitted fields from explicitly provided `null` values where clearing is supported.

---

## 6.4.4 Placement service ✅

Implemented:

- create Placement
- list Placements for a Page
- retrieve Placement
- update Placement
- delete Placement
- Page validation
- Component validation
- same-Page parent validation
- workspace scoping
- nested Placement hierarchy
- move Placement to Page root
- self-parent protection
- descendant-cycle protection
- recursive CTE cycle detection

PATCH behavior supports:

```text
parent omitted
    → keep existing parent

parent = UUID
    → assign parent

parent = null
    → move to Page root
    
# 6.4.5 Component + Placement API ✅

Implemented API endpoints for:

Components
POST   /api/v1/workspaces/{workspace_id}/components
GET    /api/v1/workspaces/{workspace_id}/components
GET    /api/v1/workspaces/{workspace_id}/components/{component_id}
PATCH  /api/v1/workspaces/{workspace_id}/components/{component_id}
DELETE /api/v1/workspaces/{workspace_id}/components/{component_id}
Placements
POST   /api/v1/workspaces/{workspace_id}/components/placements
GET    /api/v1/workspaces/{workspace_id}/components/placements
GET    /api/v1/workspaces/{workspace_id}/components/placements/{placement_id}
PATCH  /api/v1/workspaces/{workspace_id}/components/placements/{placement_id}
DELETE /api/v1/workspaces/{workspace_id}/components/placements/{placement_id}

All endpoints use workspace membership authorization.

API behavior tested:

Component creation
Component listing
Component updating
Component deletion
Placement creation
Placement listing
nested Placements
moving nested Placement to root
self-parent rejection
descendant-cycle rejection
Placement subtree cascade deletion
read-after-delete behavior
nullable PATCH field semantics

7. Automated Testing

Planned.

Scope:

Testing coverage currently includes:

unit/schema tests
database integration tests
service tests
API tests
authentication tests
authorization tests
workspace isolation tests
hierarchy/invariant tests
migration/database verification
regression coverage

automated regression testing is intentionally the next major roadmap phase
Testing becomes increasingly important as the application gains more modules.

8. Docker / Containerization

Planned.

Scope:

backend container
frontend container
PostgreSQL development environment
local development composition
environment configuration
production-oriented container practices
9. Cloud Deployment / AWS

Planned.

Scope:

production backend deployment
managed PostgreSQL
object storage
networking
secrets/configuration
domains
HTTPS
deployment architecture
10. CI/CD / GitHub Actions

Planned.

Scope:

automated tests
linting/format checks
migration checks
build validation
deployment pipeline
protected production workflow
11. Observability

Planned.

Scope:

structured logging
metrics
tracing
request correlation
error tracking
performance visibility
database monitoring
12. Reliability / Security / Queues / Background Jobs

Planned.

Scope:

background jobs
queues
retries
idempotency
rate limiting
stronger security controls
operational recovery
job visibility
13. Infrastructure as Code / Terraform

Planned.

Scope:

infrastructure configuration
reproducible environments
cloud resources managed as code
environment separation
14. Kubernetes

Planned for later.

This should only be introduced after the application has genuine operational needs that justify the additional complexity.

15. AI Fundamentals for Engineers

Planned.

Focus:

model APIs
prompting
structured outputs
embeddings
model selection
token/cost awareness
latency
retries
AI application architecture
16. RAG

Planned.

Scope:

indexing
retrieval
chunking
embeddings
vector search
metadata filtering
source attribution
knowledge scopes
17. Tool Calling

Planned.

AI should eventually interact with Personal OS through application capabilities rather than directly manipulating database tables.

18. Agents

Planned.

Future capabilities may include:

persistent agents
workspace-scoped agents
Page-scoped agents
tools
memory
knowledge scopes
schedules
triggers
permissions
approvals
autonomous actions

Agent access must follow the same authorization rules as normal application users.

19. LangChain

Planned.

Use only where it provides useful abstraction.

The core Personal OS architecture should not depend on a single AI framework.

20. LangGraph

Planned.

Potential use:

stateful workflows
multi-step agents
branching
retries
human approval
durable agent execution
21. AI Evaluation / Observability / Human-in-the-Loop

Planned.

Scope:

evaluation
traces
agent execution visibility
quality measurement
human approval
safety controls
regression testing for AI behavior
22. Production Agent Systems + Advanced Architecture + Plugin / Custom UI

Long-term stage.

Potential capabilities:

advanced agent orchestration
multi-agent systems
external AI tool integration
MCP integrations
plugin/component SDK
custom component definitions
AI-generated UI
AI page builders
user-programmable behavior
advanced permission systems
portable knowledge
external integrations
production-scale agent systems
Deferred Work

These ideas are intentionally NOT being implemented yet.

Assets

Files should eventually become first-class Assets rather than Page types.

Likely future architecture:

Asset metadata → PostgreSQL
Asset bytes → object storage
Tasks

Tasks should eventually become real domain entities rather than Page types.

A Task can then appear in multiple Pages/views.

Views

A View answers:

Given some underlying data, how should I see it?

Possible future features:

filters
sorting
grouping
table view
board view
calendar view
list view
custom presentations

The same underlying data should be able to have multiple views.

Knowledge / Context System

Planned later.

Potential scopes:

global user
workspace
Page
selection
custom scope

Knowledge should act as a lens over underlying data rather than requiring duplicate copies of the same data.

Activity / Event System

Planned later.

Activity should remain conceptually separate from knowledge.

It may record:

actions
events
usage
history
growth
temporal context
AI Page Builder

Planned later.

Potential behavior:

User describes what they want.

AI can eventually:

create Pages
create Components
create Placements
configure Views
bind data
restructure layouts

This depends on the underlying component and data model being stable enough first.

Persistent Agents

Planned later.

Agents may eventually:

live inside workspaces or Pages
have scoped knowledge
have permissions
have tools
run on schedules
respond to triggers
require approvals
modify application state
MCP

Planned later.

MCP should act as an integration boundary rather than become the core internal architecture.

Internal application services remain the authoritative capability layer.

Plugin / Component SDK

Planned later.

The initial system should use built-in components and configuration.

A future plugin system may allow:

custom component definitions
external integrations
additional capabilities
custom behavior

Arbitrary user code should not be introduced early.

Product Principles
Default simplicity

People who do not want to customize everything should still get a polished usable system.

Optional complexity

Power users should be able to progressively access deeper customization.

Total ownership

The user should own the environment and data, not merely consume a fixed application interface.

Three freedoms

The long-term Personal OS should provide:

Freedom of structure
Freedom of appearance
Freedom of behavior
Reuse underlying data

The same underlying object should be able to appear in multiple places and views without duplicating the underlying data.

Relational core + flexible configuration

Use relational database structures where relationships and integrity matter.

Use JSONB where flexible configuration is actually required.

Avoid both extremes:

rigid schemas for every visual variation
everything stored as unstructured JSON
AI operates through application capabilities

AI and agents should eventually use the same capability/service layer as normal application actions.

Authorization must still apply.

Documentation Rule

As the project evolves, this roadmap should be updated whenever:

a major phase is completed
an architectural decision changes
work is deliberately deferred
a future capability is added to the plan
an existing plan is removed

The roadmap should describe the intended system, while current-state.md records what is actually implemented.