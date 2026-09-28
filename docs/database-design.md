# Personal OS Database Design

## Core tables

### users
Represents an application user.

- id
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

### nodes
Represents a hierarchical item.

- id
- workspace_id
- parent_id
- name
- type
- created_at
- updated_at

`parent_id` references another node, allowing unlimited nesting.

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