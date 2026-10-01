# Personal OS Architecture

This document describes the current architecture and the major architectural direction of Personal OS.

The system is being built as a modular monolith first, with boundaries that can later support background workers, external integrations, AI agents, plugins, and distributed infrastructure.

---

# Core Concepts

## User

Represents a person using Personal OS.

A User can belong to multiple Workspaces.

---

## Workspace

A Workspace is the top-level application container.

It provides the primary authorization boundary for application data.

A Workspace can contain:

- Pages
- Components
- Placements
- future domain entities
- future agents
- future knowledge scopes
- future integrations

A User does not automatically receive a Workspace during registration.

---

# Universal Pages

The current hierarchical resource is conceptually called a **Page**.

It is currently represented by the `nodes` database table for historical/implementation reasons.

A Page is a universal environment or container rather than a fixed semantic type.

A Page is therefore not permanently classified as:

- folder
- note
- task
- file
- goal

Instead, those concepts can later be represented through real domain entities, Components, Views, or combinations of them.

---

# Page Hierarchy

Pages form a tree inside a Workspace.

```text
Workspace
├── Page
│   ├── Page
│   │   └── Page
│   └── Page
└── Page

A Page with parent_id = NULL is a top-level Page.

Pages can be moved while retaining their descendants.

Cycles are prevented by application-level hierarchy validation.

The database also enforces workspace ownership of parent relationships.

Page Settings

Page customization is separated from Page identity.

Page
└── PageSettings
    ├── appearance
    ├── layout_config
    └── behavior_config

Page settings are stored in a separate one-to-one table.

This prevents the Page table from becoming a large collection of visual and behavioral fields as customization grows.

Flexible settings are stored using PostgreSQL JSONB.

Components

A Component represents a reusable UI/data presentation concept.

Examples that may exist later include:

text
image
file
task-card
table
chart
calendar
custom widgets

These examples are conceptual; not all are currently implemented.

Components use an extensible definition_key rather than a fixed database enum.

Component Definitions

A future ComponentDefinition system will describe what a Component is capable of.

It may eventually contain:

definition key
version
configuration schema
capabilities
supported bindings
supported layout behavior
metadata

Built-in definitions can initially live in application code.

A future plugin/custom-component system may add externally defined components.

The ComponentDefinition system is planned but is not yet implemented.

Component vs Placement

A Component and its Placement are intentionally separate.

Component
    +
Placement
    =
Component appearing in a particular location

A single Component can have multiple Placements.

For example:

Task #123
   │
   └── Component
        ├── Placement → Dashboard → large card
        └── Placement → Today Page → compact row

This allows the same underlying data/presentation to appear differently in different places.

Component Placement

A Placement describes how a Component appears on a Page.

It can contain:

Page relationship
Component relationship
parent placement
slot
position
size
transform
style overrides
visibility
ordering

Placement hierarchy belongs to the placement instance rather than only to the abstract Component.

This allows each occurrence of a Component to have its own composition.

Data and Domain Entities

Personal OS should not turn every possible concept into a Page.

Important domain concepts should become real entities.

Examples planned for later:

Task
Asset
Person
Event
Activity

Components can then bind to those entities.

For example:

Task entity
    ↓
Task Component
    ↓
Placement on Page

This keeps the underlying data independent from its visual presentation.

Views

A future View system answers:

Given some underlying data, how should it be displayed?

A View may define:

data source
scope
filters
sorting
grouping
display configuration

Potential future views include:

list
table
board
calendar
timeline
custom views

The same underlying data should be able to appear through multiple Views without duplicating the underlying data.

Views are planned and are not yet implemented.

Assets

Files are intended to become first-class Assets rather than special Page types.

Conceptually:

Asset metadata → PostgreSQL
Asset bytes    → object storage

A future Asset can be reused by multiple Pages and Components.

The Asset system is planned and is not yet implemented.

Configuration-Driven UI

The long-term UI architecture is configuration-driven.

Instead of hardcoding every possible Page layout, the system should store enough configuration to describe:

what appears
where it appears
how it looks
how it behaves

This is the foundation for future AI-assisted Page construction.

Three Levels of Customization

The long-term Personal OS design aims to provide three broad freedoms:

Structure

Users can decide how information is organized.

Appearance

Users can control visual presentation.

Behavior

Users can control how the environment behaves and responds.

The implementation should provide sensible defaults while allowing deeper customization for power users.

AI Architecture

AI is a later layer on top of the application rather than the foundation of the database.

The intended flow is:

AI / Agent
    ↓
Application capability/service layer
    ↓
Authorization
    ↓
Database / external systems

Agents should not receive unrestricted direct database access.

They should use the same application capabilities that normal product functionality uses.

This allows authorization and validation to remain centralized.

Knowledge and Context

A future knowledge/context system will allow AI and other features to work with information at different scopes.

Potential scopes:

user
workspace
Page
selection
custom scope

Knowledge should generally act as a lens over underlying information rather than requiring duplicate copies of the same data.

The knowledge system is planned.

Activity and Events

Activity should remain conceptually separate from knowledge.

A future event/activity layer may track:

actions
events
history
usage
temporal context
system growth

This system is planned.

Agents

Future agents may exist at multiple scopes:

global/user
workspace
Page

Potential agent capabilities:

tools
memory
scoped knowledge
schedules
triggers
approvals
autonomous actions

Agents must remain subject to application authorization.

Persistent agents are planned and are not part of the current implementation.

External Integrations and MCP

MCP is intended to be an integration boundary rather than the foundation of Personal OS.

The application should first expose a clean internal capability/service layer.

External systems can then be connected through integration mechanisms such as MCP or other APIs.

MCP implementation is planned for a later stage.

Plugin and Custom Component System

The initial application should use controlled built-in components and configuration.

A later plugin/component SDK may allow:

custom component definitions
external integrations
additional capabilities
richer user customization

Arbitrary user code should not be introduced early.

Current Architecture Shape

The current conceptual architecture is:

User
  ↓
Workspace
  ↓
Pages
  ├── PageSettings
  │
  └── ComponentPlacements
        ↓
      Components
        ↓
   Data / Entities

Later systems can connect around this foundation:

Knowledge
Activity
Views
Assets
AI
Agents
Integrations
Plugins
Architectural Principles
Modular monolith first

Keep the system understandable and cohesive before introducing distributed services.

Strong relational core

Use relational tables and constraints for identity, ownership, authorization, and important relationships.

Flexible configuration where appropriate

Use JSONB for inherently flexible UI/configuration structures.

Avoid "everything is JSON"

Important domain entities and relationships should remain explicit.

Separate data from presentation

The underlying entity should not depend on where or how it is displayed.

Authorization at capability boundaries

UI actions, services, integrations, and agents must respect the same authorization rules.

Progressive complexity

Default experiences should remain simple while allowing advanced customization later.

Extensibility without premature complexity

The architecture should leave room for plugins, AI, Views, and integrations without implementing all of them immediately.


---

## 2. Replace `docs/database-design.md`

Use this:

```md
# Personal OS Database Design

This document describes the current relational database structure and the major database principles of Personal OS.

PostgreSQL is the current database.

UUIDs are used for primary identifiers.

The database is intentionally relational for important entities and relationships, while JSONB is used for flexible configuration.

---

# Core Tables

## users

Represents an application user.

Fields:

- id
- username
- email
- password_hash
- created_at
- updated_at

---

## workspaces

Represents the top-level application container.

Fields:

- id
- name
- created_at
- updated_at

---

## workspace_members

Connects Users and Workspaces.

Fields:

- id
- workspace_id
- user_id
- role
- created_at

A unique `(user_id, workspace_id)` relationship prevents duplicate membership.

Workspace membership is the current primary authorization boundary.

---

# pages / nodes

The current implementation uses the historical table name:

`nodes`

Conceptually this table now represents **Pages**.

Fields:

- id
- workspace_id
- parent_id
- name
- sort_order
- created_at
- updated_at

There is intentionally no `type` column.

A Page is therefore a universal hierarchical container.

---

# Page Hierarchy

A Page may have:

- one parent Page
- no parent Page

A NULL `parent_id` represents a top-level Page.

The database uses a workspace-aware composite relationship between:

```text
(workspace_id, parent_id)

and the parent Page's:

(workspace_id, id)

This prevents a Page from referencing a parent belonging to another Workspace.

Page Hierarchy Rules
Every Page belongs to one Workspace.
A Page may have one parent.
A top-level Page has no parent.
A parent must belong to the same Workspace.
Cycles are prevented by application-level validation.
Moving a Page keeps its descendants attached.
Deleting a Page currently deletes its descendant subtree.

An index exists for efficient workspace/parent lookups.

page_settings

Stores Page-specific appearance, layout, and behavior configuration.

Fields:

page_id
appearance
layout_config
behavior_config
created_at
updated_at

page_id is both the primary key and a foreign key to the Page.

Deleting the Page deletes its settings.

The configuration fields use PostgreSQL JSONB.

Example conceptual structure:

{
  "background": "#111111",
  "border_radius": 20
}

The exact configuration schema is expected to evolve.

components

Represents reusable Component instances.

Fields:

id
workspace_id
definition_key
config
binding
created_at
updated_at

definition_key is a string rather than a database enum so that the system can support new Component definitions without repeatedly changing the database schema.

config is JSONB.

binding is JSONB and is intended to connect a Component to underlying data or capabilities.

component_placements

Represents where and how a Component appears.

Fields:

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
Component Placement Relationships

A placement belongs to:

one Workspace
one Page
one Component
optionally one parent Placement

These relationships use workspace-aware composite foreign keys where appropriate.

This ensures that a placement cannot accidentally cross Workspace boundaries.

Placement Configuration

The following fields use JSONB:

position
size
transform
style

The purpose is to support multiple layout/composition models without forcing one permanent database representation.

For example, different layout systems may eventually use:

flow layouts
grids
canvas positioning
stacks
custom layouts

The database should not need a schema change every time a new visual composition capability is introduced.

Database Relationships

Current conceptual relationships:

User
  ↓
WorkspaceMember
  ↓
Workspace
  ├── Page
  │    └── Page
  │
  ├── PageSettings
  │
  ├── Component
  │
  └── ComponentPlacement
       ├── Page
       ├── Component
       └── Parent Placement
Cascade Rules

Important ownership relationships currently use cascade deletion where appropriate.

Examples:

Workspace
  ↓
Pages

Page
  ↓
PageSettings

Page
  ↓
ComponentPlacements

Component
  ↓
ComponentPlacements

ComponentPlacement
  ↓
Child ComponentPlacements

Cascade behavior should always be tested before relying on it for destructive workflows.

Future Domain Tables

The following are expected to become real relational entities later rather than Page types.

tasks

Potential future fields include:

id
workspace_id
title
status
priority
due_at
created_by
timestamps

The exact model is intentionally deferred.

assets

A future Asset system is expected to contain metadata such as:

id
workspace_id
created_by
filename
mime_type
size_bytes
storage_key
checksum
metadata
timestamps

File bytes are expected to move to object storage while PostgreSQL stores metadata.

people

A future domain entity for people/contacts may be introduced if product requirements require it.

events / activity

A future event/activity system may store:

actions
events
timestamps
actor
target
metadata

The activity system should remain separate from the knowledge system.

Future Views

Views are expected to reference underlying data rather than duplicate it.

Potential View configuration may contain:

source
scope
filters
sorting
grouping
display configuration

Views are not currently implemented.

JSONB Usage Principle

JSONB is intentionally used for areas where variation is expected.

Current examples:

Page appearance
Page layout configuration
Page behavior configuration
Component configuration
Component binding
Placement position
Placement size
Placement transform
Placement style

JSONB should not replace normal relational modeling for:

identity
authorization
ownership
important cross-record relationships
core domain entities
Migration Management

Alembic is used for schema migrations.

Each schema change should be:

represented in SQLAlchemy models
generated/verified through Alembic
inspected before application
applied to the development database
checked with alembic current
checked with alembic check
committed to version control
Current Database Direction

The current database foundation is intentionally small.

The database should grow through well-defined domain entities rather than through one generic table containing arbitrary JSON.

The long-term architecture therefore follows:

Relational identity + relationships
              +
     flexible JSONB configuration
              +
       external object storage
              +
       future indexing/search

rather than:

Everything → one generic JSON table

This preserves data integrity while keeping the UI and configuration layer extensible.