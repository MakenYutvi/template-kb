# Журнал контекста

Журнал значимых изменений контекста.

## Формат записи

Используйте формат:

```text
## YYYY-MM-DD | kind | short-title
```

Примеры `kind`: `setup`, `ingest`, `writeback`, `decision`, `project`, `cleanup`.

## 2026-11-17 | decision | optional-prompts-and-automation-setup

- Scope: переносимые prompts для документов, продуктовой работы, проверки KB и обслуживания чатов/Git.
- Sources: [каталог](../prompts/README.md), [рецепты](../docs/automation-recipes.md).
- Outcome: setup/upgrade предлагают автоматизации; режим, параметры и права выбирает пользователь. Существующие задания и локальные prompts сохраняются. Приватные проектные задания и служебные runners не включены.
- Checks: [случаи сохранности и режимов](../docs/workflow-checks.md); границы фактической проверки — [CHANGELOG](../CHANGELOG.md).

## 2026-11-16 | decision | light-memory-workflows

- Scope: публичный template, без пользовательских sources и экспериментальной инфраструктуры.
- Sources: [решение](decisions/2026-11-16-light-memory-workflows.md), [синтетические cases](../docs/workflow-checks.md).
- Updated: правила, context-budget/writeback, compact prompt, upgrade prompt и связанные entrypoints/docs.
- Optional: практические prompts сохранения сессии, восстановления задачи и review документа; рецепты локальной проверки и запуска выбранных задач. Расписания не включены, периодический обзор по умолчанию только возвращает отчёт.
- Outcome: явный no-op повтора, сохранение истории и локальных правил; учёт, модель и расписания не требуются. Исправлена комплектация `wiki/outputs/`, setup и upgrade сохраняют entrypoints ОС по умолчанию; пользовательские индексы и ignore-исключения не заменяются шаблоном.
- Follow-up: ограничения и результаты проверок — в [CHANGELOG](../CHANGELOG.md); агентский A/B-прогон не выполнялся.

## 2026-06-24 | setup | memory-workflows-upgrade

- Scope: template repository setup.
- Sources: mature KB operational patterns, адаптированные без private source content.
- Updated: `wiki/outputs/`, `wiki/health/`, `wiki/people/`, `indexes/meetings.md`, `indexes/people-relations.md`, meeting source stubs, workflow docs, prompts, helper scripts и lint checks.
- Outcome: шаблон поддерживает cycle `source -> triage -> ingest/compile -> wiki -> query/output -> writeback -> lint/health`, substantial outputs, health reports, golden eval, prompt-injection-aware meeting ingest и merge-first upgrade prompt.
- Follow-up: проверить upgrade на персонализированной KB без перезаписи пользовательского контента.

## 2026-06-03 | setup | helper-scripts-and-claude

- Scope: template repository setup.
- Sources: local template evolution; Karpathy LLM Wiki reference.
- Updated: `scripts/`, `prompts/`, `README.md`, `SETUP.md`, `CLAUDE.md`, `.ai/tool-profiles/claude.md`, navigation files.
- Outcome: добавлены setup doctor, KB item generator, source digest manager, три operational prompts и Claude adapter.
- Follow-up: проверить, нужен ли optional meetings pack в следующей итерации.

## 2026-06-03 | setup | scripts-and-lint

- Scope: template repository setup.
- Sources: mature knowledge base operational patterns, адаптированные без private source content.
- Updated: `scripts/`, `SETUP.md`, `wiki/workflows/`, `wiki/decisions/`, `prompts/`, `README.md`, `AGENTS.md`, `.ai/contract.md`.
- Outcome: добавлены локальные проверки, pre-commit installer, setup checklist, helper-script prompt и расширенные wiki workflows.
- Follow-up: проверить lint на чистом clone после персонализации первого пользователя.

## YYYY-MM-DD | setup | initial-template

- Scope: repository setup.
- Sources: template repository.
- Updated: initial `README.md`, `AGENTS.md`, `raw/`, `wiki/`, `.ai/`.
- Outcome: создана стартовая структура личной knowledge base.
- Follow-up: персонализировать репозиторий и добавить первый source-файл.
