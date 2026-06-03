# Context Log

Журнал значимых изменений контекста.

## Формат записи

Используйте формат:

```text
## YYYY-MM-DD | kind | short-title
```

Примеры `kind`: `setup`, `ingest`, `writeback`, `decision`, `project`, `cleanup`.

## 2026-06-03 | setup | scripts-and-lint

- Scope: template repository setup.
- Sources: mature knowledge base operational patterns, adapted without private source content.
- Updated: `scripts/`, `SETUP.md`, `wiki/workflows/`, `wiki/decisions/`, `prompts/`, `README.md`, `AGENTS.md`, `.ai/contract.md`.
- Outcome: добавлены локальные проверки, pre-commit installer, setup checklist, helper-script prompt и расширенные wiki workflows.
- Follow-up: проверить lint на чистом clone после персонализации первого пользователя.

## YYYY-MM-DD | setup | initial-template

- Scope: repository setup.
- Sources: template repository.
- Updated: initial `README.md`, `AGENTS.md`, `raw/`, `wiki/`, `.ai/`.
- Outcome: создана стартовая структура личной knowledge base.
- Follow-up: персонализировать репозиторий и добавить первый source-файл.
