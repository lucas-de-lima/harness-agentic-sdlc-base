# GitHub MCP — Phase 14 Contract

## Current strategy

Use GitHub's official MCP server rather than building a custom GitHub MCP.

GitHub maintains an official MCP server, and its toolsets can be selectively enabled. citeturn501381search7

## Required capability set

Initial capabilities:

- read issue
- search/list issues
- inspect parent/sub-issues
- read Project state
- add execution comment
- update task status when authorized

Project-specific Projects tools may require enabling the Projects toolset explicitly; the official server exposes Projects capabilities separately. citeturn501381search5

## Least privilege

Discovery:

- GitHub read-only

Orchestrator:

- read issues/projects
- controlled status/comment writes

Developer:

- read work state
- write evidence associated with the task

Reviewer:

- read-only plus review comments

## No broad write access

Do not enable broad repository mutation for the first integration.

## Authentication

The official server supports stdio configuration with a GitHub token and can also be run via containerized tooling. Follow the host-specific authentication guidance at implementation time. citeturn501381search7
