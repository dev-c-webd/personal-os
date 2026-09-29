# Personal OS Database Design

## Core tables

### users
Represents an application user.

- id
- username
- email
- password_hash
- created_at
- updated_at


### workspaces
Represents a container for a user's system.

- id
- name
- created_at
- updated_at


### workspace_members
Connects users and workspaces.

- id
- workspace_id
- user_id
- role
- created_at


## nodes

A node is a generic hierarchical item inside a workspace.

Fields:
- id
- workspace_id
- parent_id
- name
- type
- sort_order
- created_at
- updated_at

`parent_id` references another node and allows unlimited nesting.

A NULL parent_id represents a top-level node.

A node's parent must belong to the same workspace.

Node types initially include:
- folder
- file
- note
- task
- goal

## Node hierarchy rules

- Nodes belong to one workspace.
- A node may have one parent or no parent.
- A parent must belong to the same workspace.
- Cycles must not be allowed.
- Moving a node changes its parent; descendants remain attached to it.


### files
Stores metadata for file nodes.

- id
- node_id
- storage_key
- original_name
- mime_type
- size_bytes
- created_at
- updated_at


## Relationships

User
  ↓
WorkspaceMember
  ↓
Workspace
  ↓
Node

Node
  └── parent_id → Node.id

Node (type=file)
  ↓
File

