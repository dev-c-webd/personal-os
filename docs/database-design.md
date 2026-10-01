# Personal OS Database Design

This document describes the current relational database structure and the major database principles of Personal OS.

PostgreSQL is the current database.

UUIDs are used for primary identifiers.

The database is intentionally relational for important entities and relationships, while JSONB is used for flexible configuration.

---

# Core Tables

## `users`

Represents an application user.

Fields:

- `id`
- `username`
- `email`
- `password_hash`
- `created_at`
- `updated_at`

---

## `workspaces`

Represents the top-level application container.

Fields:

- `id`
- `name`
- `created_at`
- `updated_at`

A Workspace is currently the main authorization boundary for application data.

---

## `workspace_members`

Connects Users and Workspaces.

Fields:

- `id`
- `workspace_id`
- `user_id`
- `role`
- `created_at`

A unique `(user_id, workspace_id)` relationship prevents duplicate membership.

Workspace membership is the current primary authorization mechanism for workspace-scoped resources.

---

# `nodes` — Universal Pages

The current implementation uses the historical table name:

`nodes`

Conceptually, this table now represents **Pages**.

Fields:

- `id`
- `workspace_id`
- `parent_id`
- `name`
- `sort_order`
- `created_at`
- `updated_at`

There is intentionally **no `type` column**.

A Page is therefore a universal hierarchical container.

Pages are not permanently classified as:

- folder
- file
- note
- task
- goal

Those concepts can later become real domain entities, Components, Views, or combinations of these.

---

# Page Hierarchy

A Page may have:

- one parent Page
- no parent Page

A `NULL parent_id` represents a top-level Page.

The database uses a workspace-aware composite foreign key between:

```text
(workspace_id, parent_id)

and the parent's:

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

An index exists on workspace and parent information to support efficient child lookups.

page_settings

Stores Page-specific appearance, layout, and behavior configuration.

Fields:

page_id
appearance
layout_config
behavior_config
created_at
updated_at

page_id is both:

the primary key
a foreign key to nodes.id

This gives the Page Settings table a one-to-one relationship with a Page.

Deleting a Page deletes its settings.

The configuration fields use PostgreSQL JSONB.

Example conceptual structure:

{
  "background": "#111111",
  "border_radius": 20
}

The exact configuration schema is expected to evolve as the customization system develops.

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

definition_key is a string rather than a database enum so that new Component definitions can be introduced without repeatedly changing the database schema.

config is stored as JSONB.

binding is also stored as JSONB and is intended to connect a Component to underlying application data or capabilities.

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

A Placement describes a particular occurrence of a Component on a Page.

Component Placement Relationships

A Placement belongs to:

one Workspace
one Page
one Component
optionally one parent Placement

The database uses workspace-aware composite foreign keys for these relationships.

This ensures that a Placement cannot accidentally reference:

a Page from another Workspace
a Component from another Workspace
a parent Placement from another Workspace
Placement Hierarchy

Placements can contain other Placements through:

parent_placement_id

This allows Components to eventually act as containers for other Components.

The hierarchy is attached to the Placement instance rather than only to the abstract Component.

This allows the same Component to appear in different locations with different compositions.

Placement Configuration

The following fields use JSONB:

position
size
transform
style

This is intentional.

The application is expected to support multiple composition/layout models over time, such as:

flow
grid
canvas
stack
custom layouts

The database should not require a schema change every time a new visual composition capability is introduced.

Current Relationships

The current conceptual relationship structure is:

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
Ownership and Cascades

Important ownership relationships use cascade deletion where appropriate.

Conceptually:

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

Destructive cascade behavior should continue to be covered by tests as the application grows.

Future Domain Tables

The following concepts are expected to become real relational entities later.

They are intentionally not being implemented as Page types.

tasks

A future Task entity may contain information such as:

id
workspace_id
title
status
priority
due_at
created_by
timestamps

The exact schema is intentionally deferred.

assets

Files are intended to become first-class Assets.

A future Asset table may contain:

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

The expected architecture is:

Asset metadata → PostgreSQL
Asset bytes    → Object Storage

The Asset system is not implemented yet.

People

A future domain entity for people or contacts may be introduced when required by the product.

Events / Activity

A future activity/event system may store:

actor
event type
target
timestamp
metadata

Activity is intended to remain conceptually separate from the Knowledge system.

Future Views

Views are expected to provide different ways of displaying the same underlying data.

A future View configuration may contain:

source
scope
filters
sorting
grouping
display configuration

Potential View types may include:

list
table
board
calendar
timeline
custom views

Views are not currently implemented.

JSONB Usage Principle

JSONB is intentionally used where configuration is expected to be flexible.

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
Avoid "Everything Is JSON"

The database should not become one generic table containing arbitrary JSON for everything.

Important application concepts should remain explicit relational entities.

The intended direction is:

Relational identity + relationships
              +
     Flexible JSONB configuration
              +
        Object storage
              +
       Future indexing/search

rather than:

Everything → one generic JSON table
Migration Management

Alembic is used for schema migrations.

A schema change should generally follow this process:

Update the SQLAlchemy model.
Generate an Alembic migration.
Inspect the generated migration.
Adjust it when required.
Apply the migration to the development database.
Verify the current migration revision.
Run alembic check.
Commit the migration and model changes together.
Current Database Direction

The current database foundation is intentionally small.

The schema should grow through well-defined domain entities and relationships rather than through a single generic JSON structure.

The long-term database strategy is therefore:

Strong relational core
        +
Flexible configuration
        +
External object storage
        +
Future search/indexing

This preserves data integrity while keeping the Personal OS UI and behavior extensible.