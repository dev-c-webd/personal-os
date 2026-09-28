# Personal OS Architecture

## Core concepts

User
- Represents a person using the system.

Workspace
- Container for a user's organizational system.

Node
- Generic hierarchical item inside a workspace.
- Nodes can have child nodes through parent_id.
- Node types may include folder, file, note, task and goal.

File
- Stores metadata about a file represented by a file node.
- Actual file contents will eventually be stored in object storage.

## Core hierarchy

User
    ↓
Workspace
    ↓
Node
    ↓
Child Node
    ↓
Child Node


# It will represented as:

User
  ↓
Workspace
  ↓
Node
  ├── Folder
  ├── File
  ├── Note
  ├── Task
  └── Goal