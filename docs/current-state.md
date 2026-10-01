# Personal OS — Current State

This document records the actual implementation state of the Personal OS repository.

It should describe what exists in the codebase and database, not merely what is planned.

---

## Current Roadmap Position

Current major roadmap stage:

**Roadmap 6 — Personal OS Resources**

Current sub-phase:

**6.4 — Component System**

Current implementation point:

**6.4.3 — Component service**

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

Backend stack currently includes:

Python
FastAPI
SQLAlchemy
PostgreSQL
Alembic
Pydantic
JWT authentication
Argon2 password hashing
uv for Python dependency/environment management
API Structure

The API uses versioned routes:

/api/v1/...

Existing major API areas include:

/auth
/users
/workspaces
/workspaces/{workspace_id}/nodes

Page-related functionality is currently represented through the existing nodes API.

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

Workspace operations use membership verification before protected operations are performed.

Database

Current PostgreSQL database contains the foundational application tables and the evolving Personal OS data model.

Core tables implemented:

users
workspaces
workspace_members
nodes
page_settings
components
component_placements
User

The User model currently contains:

UUID id
username
email
password hash
created timestamp
updated timestamp
Workspace

The Workspace model currently contains:

UUID id
name
created timestamp
updated timestamp

A user can belong to multiple workspaces.

Registration does not automatically create a workspace.

Workspace Membership

Workspace membership is represented separately from User and Workspace.

Current membership information includes:

UUID id
workspace_id
user_id
role
created timestamp

A unique user/workspace relationship is enforced.

Workspace membership is also the current authorization boundary.

Pages

Pages are currently represented by the nodes database table.

A Page contains:

UUID id
workspace_id
parent_id
name
sort_order
created timestamp
updated timestamp

Pages no longer have a fixed semantic type.

The system therefore does NOT currently classify Pages as:

folders
files
notes
tasks
goals

A Page is a universal hierarchical container.

Page Hierarchy

Pages support:

unlimited nesting
top-level Pages
child Pages
moving Pages
moving Pages back to the workspace root
sibling ordering

Database-level protection ensures a Page cannot reference a parent from another workspace.

Application-level recursive logic prevents cycles.

Deleting a Page currently deletes its descendant subtree.

Page Settings

Page customization is represented separately through:

page_settings

Current configuration sections:

appearance
layout_config
behavior_config

These are stored as PostgreSQL JSONB.

The settings record is associated one-to-one with a Page.

Current API behavior:

GET settings
PATCH settings
lazy creation of default settings
workspace authorization
Page existence validation

A newly accessed Page can receive default settings:

{
  "appearance": {},
  "layout_config": {},
  "behavior_config": {}
}
Component System

The Component system is currently being implemented.

The current database contains:

components
component_placements
Component

A Component represents a reusable UI/data presentation concept.

Current fields include:

id
workspace_id
definition_key
config
binding
created_at
updated_at

definition_key is a string rather than a database enum.

Examples of future definition keys could include:

text
image
task-card
table
chart
file

These examples are conceptual and are not all implemented yet.

Component Configuration

config is stored as JSONB.

This allows component-specific configuration without requiring a new database column for every possible UI option.

Component Binding

binding is stored as JSONB.

It is intended to connect a Component to underlying data or another application capability.

Examples of future bindings could reference:

tasks
assets
people
events
views

The generic binding system is currently only foundational; those domain entities are not all implemented yet.

Component Placement

A Component and its Placement are separate concepts.

A Placement describes how a Component is used on a particular Page.

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

The flexible visual properties use JSONB.

Placement Hierarchy

Placements can have parent placements.

This allows Components to eventually be nested inside containers/components.

The database uses workspace-aware composite foreign keys so that:

a Placement cannot point to a Page in another workspace
a Placement cannot point to a Component in another workspace
a Placement cannot point to a parent Placement in another workspace
Component Schemas

Currently implemented:

ComponentCreate
ComponentUpdate
ComponentResponse

ComponentPlacementCreate
ComponentPlacementUpdate
ComponentPlacementResponse

Schemas use UUIDs and Pydantic validation.

Flexible configuration fields use dictionaries compatible with JSON data.

Component Service

Current Component service functionality:

create_component
get_components
get_component_by_id
update_component
delete_component

All operations are workspace-scoped.

The service has been import-tested.

Placement service and Component API routes have not yet been implemented in the current phase.

Important Architectural Distinctions
Page

Represents the universal environment/container in the user's hierarchy.

Component

Represents a reusable thing that can be presented.

Placement

Represents where and how a Component is placed on a Page.

Underlying Data

The long-term design allows Components to represent or display actual domain entities without making those entities into Page types.

Implemented vs Planned
Implemented
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
initial Component service
Not yet implemented
Placement service
Component API
Placement API
automated Component tests
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

The following have intentionally been left for later instead of being prematurely implemented:

Assets

File metadata should eventually live in PostgreSQL while file bytes can live in object storage.

Tasks

Tasks should become real domain entities rather than Page types.

Views

Views should provide different presentations of the same underlying data.

Knowledge

Knowledge should support multiple scopes and work as a lens over underlying application data.

Activity

Activity/event tracking should remain separate from the knowledge system.

AI

AI should operate through application capabilities/services rather than directly manipulating database tables.

Agents

Agents should inherit the same authorization boundaries as normal application actions.

MCP

MCP should be treated as an integration boundary rather than the foundation of the internal application architecture.

Plugins

Arbitrary user code should not be introduced early. A controlled component/plugin system can be added later.

Documentation Status

The documentation is currently being migrated from the earlier Node/type-based design to the current universal Page + Component architecture.

The following documents require synchronization with the current architecture:

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

The repository documentation should eventually become the durable source of truth for:

architecture
roadmap
current implementation
architectural decisions
deferred work

The conversation is used for working through implementation details, but important long-term decisions should be transferred into the repository.