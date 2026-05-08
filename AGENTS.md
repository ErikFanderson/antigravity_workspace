# Workspace Rules

## Python Environment Setup

Always source the `activate_all.sh` script at the beginning of a conversation before running any Python-related commands. This ensures the correct pyenv version and virtual environment are active.

### Instructions for the Agent
1. **Start Persistent Shell**: Use `run_command` with `RunPersistent: true` to initiate a session.
2. **Source Setup**: Run `source activate_all.sh` as the first command in that persistent shell.
3. **Persist State**: For all subsequent Python or shell commands in the same conversation, reuse the same `TerminalID` to maintain the environment state.
4. **No Redundancy**: Do not re-source the script for every command; the persistent shell will keep the environment active once sourced.

## Google API Access

Use the credentials in `credentials/google` to access Google APIs for any requests to edit or create Google Slides, Sheets, or Docs on Google Drive.

### Instructions for the Agent
1. **Credentials Path**: Use the `client_secret.json` and `token.json` found in `credentials/google` for authentication.
2. **Scope**: This applies to all Google Drive and Workspace (Slides, Sheets, Docs) API operations.

## Reusable Workspace Functions

Agents should utilize the local Python module `src/antigravity_workspace` to create and access reusable functions for interacting with APIs (e.g., Google Slides, Sheets, Docs) using the credentials in the `credentials/` folder.

### Instructions for the Agent
1. **Prefer Module Over One-off Scripts**: Instead of writing standalone scripts for every task, implement reusable logic within `src/antigravity_workspace`.
2. **Accessing Functions**: Import from `antigravity_workspace` to leverage existing API interaction logic (e.g., `from antigravity_workspace.google_slides_creator import get_services`).
3. **Standardized Credential Access**: Use the module to ensure consistent handling of credentials and token paths.
