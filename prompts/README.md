# Prompts

Reusable prompts are task templates that can be copied into an AI chat or wrapped by a tool-specific command.

This folder is tool-neutral: prompts here should not depend on Codex, Cursor, Claude Code, or a specific local path. Put repository-specific paths, project names, people, and constraints into the prompt input when using the template.

## Format

Each prompt file should contain only the executable instruction. Do not add metadata headers, frontmatter, `# name`, `# description`, or wrapper comments. The prompt name is the file name; the purpose is documented in the catalog below.

Recommended sections:

- `Role` - who the model should act as.
- `Input` - what the user should provide.
- `Output` - expected result and structure.
- `Process` - ordered steps, if the task needs them.

File names should use `kebab-case.md`.

## Catalog

| Prompt | Purpose |
|---|---|
| [`setup-new-kb.md`](setup-new-kb.md) | Prompt for personalizing a new repository created from this template. |
| [`create-kb-helper-script.md`](create-kb-helper-script.md) | Prompt for adding a small local helper script with wrappers, docs and verification. |
| [`ingest-source.md`](ingest-source.md) | Prompt for ingesting one new source file into durable wiki memory. |
| [`review-kb-diff.md`](review-kb-diff.md) | Prompt for reviewing repository diff before commit. |
| [`weekly-review.md`](weekly-review.md) | Prompt for a periodic maintenance review of the knowledge base. |
| [`web-chat-to-kb-transfer.md`](web-chat-to-kb-transfer.md) | Short copy-paste prompt for preparing a two-part transfer package from the current web GPT chat. |
| [`web-gpt-global-context-to-kb-transfer.md`](web-gpt-global-context-to-kb-transfer.md) | Short copy-paste prompt for preparing a two-part transfer package from global web GPT context. |

## Quick Start For Transfer Prompts

By default, copy the main compact prompt directly into web GPT:

```powershell
Get-Content -Raw -Encoding UTF8 -LiteralPath .\prompts\web-chat-to-kb-transfer.md | Set-Clipboard
```

For global context:

```powershell
Get-Content -Raw -Encoding UTF8 -LiteralPath .\prompts\web-gpt-global-context-to-kb-transfer.md | Set-Clipboard
```

Web GPT should produce two blocks: `КОРОТКАЯ КОМАНДА ДЛЯ CODEX` and `TRANSFER PAYLOAD`. In Codex, send the short command first, then send the payload or a `.txt` file with the payload as a second message.
