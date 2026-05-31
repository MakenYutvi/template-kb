# Context Log

Журнал значимых изменений контекста.

## Формат записи

Используйте формат:

```text
## YYYY-MM-DD | kind | short-title
```

Примеры `kind`: `setup`, `ingest`, `writeback`, `decision`, `project`, `cleanup`.

## YYYY-MM-DD | setup | initial-template

- Scope: repository setup.
- Sources: template repository.
- Updated: initial `README.md`, `AGENTS.md`, `raw/`, `wiki/`, `.ai/`.
- Outcome: создана стартовая структура личной knowledge base.
- Follow-up: персонализировать репозиторий и добавить первый source-файл.
