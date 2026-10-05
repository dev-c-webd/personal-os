# Personal OS — Current State

This document records the actual implementation state of the Personal OS repository.

It describes what currently exists, what has been tested, and what remains planned or deferred.

---

## Current Roadmap Position

Current major roadmap stage:

**Roadmap 7 — Automated Testing**

Completed immediately before this stage:

Roadmap 7 — Automated Testing ✅

7.1 Test infrastructure ✅
7.2 Database/service integration testing ✅
7.3 API testing ✅
7.4 Authentication & authorization testing ✅

Automated test suite: 37 tests passing.

Current testing coverage includes:
- schema/unit tests
- database integration tests
- service tests
- API tests
- authentication
- authorization
- workspace isolation
- hierarchy invariants
- recursive deletion behavior
- regression coverage

**Roadmap 6 → 6.4 — Component System**

---

# Repository Structure

```text
personal-os/
├── backend/
├── frontend/
├── docs/
├── .gitignore
└── README.md
Backend

Current backend stack:

Python
FastAPI
SQLAlchemy
PostgreSQL
Alembic
Pydantic
JWT authentication
Argon2 password hashing
uv for Python dependency/environment management
API

The API uses:

/api/v1/...

Current major API areas include:

authentication
users
workspaces
Pages through the nodes API
Page settings
Components
Component Placements
Authentication

Implemented:

user registration
user login
password hashing
JWT authentication
current authenticated-user dependency

Authorization foundation:

workspace membership
workspace-scoped access control

Protected workspace resources use workspace membership verification.

Database

Current core tables:

users
workspaces
workspace_members
nodes
page_settings
components
component_placements

PostgreSQL is the database.

UUIDs are used for primary identifiers.

Relational structures are used for important identity, ownership, and relationships.

JSONB is used for flexible configuration.

Users

The User model contains:

UUID id
username
email
password hash
created timestamp
updated timestamp
Workspaces

The Workspace model contains:

UUID id
name
created timestamp
updated timestamp

A User can belong to multiple Workspaces.

Registration does not automatically create a Workspace.

Workspace Membership

Workspace membership connects Users and Workspaces.

Current information includes:

UUID id
workspace_id
user_id
role
created timestamp

A unique user/workspace relationship is enforced.

Workspace membership is the current primary authorization boundary.

Pages

Pages are currently represented by the historical nodes table.

A Page contains:

UUID id
workspace_id
parent_id
name
sort_order
created timestamp
updated timestamp

Pages no longer have a semantic type.

A Page is a universal hierarchical container.

Page Hierarchy

Implemented:

unlimited nesting
top-level Pages
child Pages
Page movement
moving Pages back to workspace root
sibling ordering
workspace-aware parent protection
application-level cycle prevention
recursive subtree deletion

Deleting a Page currently deletes its descendant subtree.

Page Settings

Implemented through:

page_settings

Configuration sections:

appearance
layout_config
behavior_config

These are stored as PostgreSQL JSONB.

Implemented behavior:

GET settings
PATCH settings
lazy creation of default settings
Page existence validation
workspace authorization
Component System

The Component System is implemented through:

components
component_placements

The system is designed around:

Component
    +
Placement
    =
Component appearing on a Page

A Component can have multiple Placements.

Components

Current fields include:

id
workspace_id
definition_key
config
binding
created_at
updated_at

definition_key is a string rather than a database enum.

config uses JSONB.

binding uses JSONB.

Component operations implemented:

create
list
retrieve
update
delete

All operations are workspace-scoped.

Component Placement

Current fields include:

id
workspace_id
page_id
component_id
parent_placement_id
slot_key
position
size
transform
style
visible
sort_order
created_at
updated_at

Flexible visual/configuration fields use JSONB.

Placement Hierarchy

Implemented:

root Placements
nested Placements
Page-level Placement listing
parent Placement validation
same-Page parent validation
workspace isolation
self-parent protection
descendant-cycle protection
recursive CTE cycle detection
moving a Placement back to Page root
cascade deletion of child Placements

PATCH semantics distinguish between:

field omitted
    → leave existing value unchanged

field = UUID
    → assign value

field = null
    → explicitly clear nullable relationship/value

This behavior is implemented for the relevant nullable fields.

Component Schemas

Implemented:

ComponentCreate
ComponentUpdate
ComponentResponse
ComponentPlacementCreate
ComponentPlacementUpdate
ComponentPlacementResponse

Schemas use Pydantic validation and UUID identifiers.

Component API

Implemented Component endpoints:

POST   /api/v1/workspaces/{workspace_id}/components
GET    /api/v1/workspaces/{workspace_id}/components
GET    /api/v1/workspaces/{workspace_id}/components/{component_id}
PATCH  /api/v1/workspaces/{workspace_id}/components/{component_id}
DELETE /api/v1/workspaces/{workspace_id}/components/{component_id}

Implemented Placement endpoints:

POST   /api/v1/workspaces/{workspace_id}/components/placements
GET    /api/v1/workspaces/{workspace_id}/components/placements
GET    /api/v1/workspaces/{workspace_id}/components/placements/{placement_id}
PATCH  /api/v1/workspaces/{workspace_id}/components/placements/{placement_id}
DELETE /api/v1/workspaces/{workspace_id}/components/placements/{placement_id}

All endpoints use workspace membership authorization.

Component System Testing Status

Manual API behavior has been verified for:

Component creation
Component listing
Component update
Component deletion
read-after-delete
root Placement creation
Placement listing
nested Placement creation
nested-to-root movement
self-parent rejection
descendant-cycle rejection
Placement subtree cascade deletion
nullable PATCH behavior


Implemented

The current implementation includes:

FastAPI backend
PostgreSQL
SQLAlchemy
Alembic
authentication
workspace model
workspace membership
workspace authorization foundation
universal Pages
Page hierarchy
Page movement
cycle prevention
recursive subtree deletion
Page settings
Component models
Component database migration
Component schemas
Component service
Placement service
Component API
Placement API
manual API behavior testing

# It should instead say that automated testing is implemented through 31 passing tests, while the remaining testing work is future expansion as new modules are introduced.

Not Yet Implemented

The following are planned but not yet implemented:

Asset entity
object/file storage
Task entity
View system
Knowledge system
activity/event system
AI page builder
persistent agents
MCP integrations
plugin/component SDK
advanced customization system
cloud deployment
CI/CD
observability
queues/background jobs
Kubernetes
production AI infrastructure
Important Deferred Decisions
Assets

File metadata should eventually live in PostgreSQL while file bytes can live in object storage.

Tasks

Tasks should become real domain entities rather than Page types.

Views

Views should provide different presentations of the same underlying data.

Knowledge

Knowledge should support multiple scopes and work as a lens over underlying information.

Activity

Activity/event tracking should remain separate from the Knowledge system.

AI

AI should operate through application capabilities/services rather than directly manipulating database tables.

Agents

Agents should inherit the same authorization boundaries as normal application actions.

MCP

MCP should be treated as an integration boundary rather than the foundation of the internal application architecture.

Plugins

Arbitrary user code should not be introduced early. A controlled plugin/component system can be added later.

Documentation Status

The primary architecture documentation has been synchronized with the current universal Page + Component architecture.

Current core documentation:

docs/roadmap.md
docs/current-state.md
docs/architecture.md
docs/database-design.md

Additional documentation planned:

docs/product-vision.md
docs/api-design.md
docs/security-and-permissions.md
docs/ui-and-customization.md
docs/knowledge-and-context.md
docs/ai-and-agents.md
docs/integrations-and-mcp.md
docs/performance-and-scalability.md
docs/changelog.md
docs/decisions/
Source of Truth

The repository documentation is the durable source of truth for:

architecture
roadmap
current implementation
architectural decisions
deferred work

The conversation is used for working through implementation details, but important long-term decisions should be transferred into the repository.