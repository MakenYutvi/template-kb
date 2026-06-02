# Prompts

Reusable prompts are task templates that can be copied into an AI chat or wrapped by a tool-specific command.

This folder is tool-neutral: prompts here should not depend on Codex, Cursor, Claude Code, or a specific local path. Put repository-specific paths, project names, people, and constraints into the prompt input when using the template.

## Format

Each prompt should start with:

```markdown
# name: <kebab-case-id>
# description: <one-line purpose>
```

Recommended sections:

- `Role` - who the model should act as.
- `Input` - what the user should provide.
- `Output` - expected result and structure.
- `Process` - ordered steps, if the task needs them.

File names should use `kebab-case.md`.

## Catalog

| Prompt | Purpose |
|---|---|
| [`web-chat-to-kb-transfer.md`](web-chat-to-kb-transfer.md) | Prepare a two-part transfer package for moving current web GPT chat context into a local knowledge base, robust to payload auto-conversion into `.txt`. |
| [`web-gpt-global-context-to-kb-transfer.md`](web-gpt-global-context-to-kb-transfer.md) | Prepare a two-part transfer package for moving global web GPT context into a local knowledge base, robust to payload auto-conversion into `.txt`. |
