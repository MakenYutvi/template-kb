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
| [`web-chat-to-kb-transfer-launcher.md`](web-chat-to-kb-transfer-launcher.md) | Short launcher command for running `web-chat-to-kb-transfer.md` when the main template is attached as a file in web GPT. |
| [`web-chat-to-kb-transfer.md`](web-chat-to-kb-transfer.md) | Short copy-paste prompt for preparing a two-part transfer package from the current web GPT chat. |
| [`web-gpt-global-context-to-kb-transfer-launcher.md`](web-gpt-global-context-to-kb-transfer-launcher.md) | Short launcher command for running `web-gpt-global-context-to-kb-transfer.md` when the main template is attached as a file in web GPT. |
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

If web GPT still turns the prompt into a `.txt` or attachment, use the fallback: send the short launcher as a text message and attach the main prompt file.

1. For the current chat: copy [`web-chat-to-kb-transfer-launcher.md`](web-chat-to-kb-transfer-launcher.md) into the message and attach [`web-chat-to-kb-transfer.md`](web-chat-to-kb-transfer.md).
2. For global context: copy [`web-gpt-global-context-to-kb-transfer-launcher.md`](web-gpt-global-context-to-kb-transfer-launcher.md) into the message and attach [`web-gpt-global-context-to-kb-transfer.md`](web-gpt-global-context-to-kb-transfer.md).
3. Web GPT should produce two blocks: `КОРОТКАЯ КОМАНДА ДЛЯ CODEX` and `TRANSFER PAYLOAD`.
4. In Codex, send the short command first, then send the payload or a `.txt` file with the payload as a second message.
