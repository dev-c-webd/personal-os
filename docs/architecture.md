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