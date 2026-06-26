# Карта знаний

Навигационная карта репозитория.

## Главные входы

- [`../README.md`](../README.md) - быстрый старт и структура.
- [`../SETUP.md`](../SETUP.md) - checklist первичной настройки.
- [`../AGENTS.md`](../AGENTS.md) - инструкции AI-агенту.
- [`../CLAUDE.md`](../CLAUDE.md) - тонкий adapter для Claude Code.
- [`../wiki/current-status.md`](../wiki/current-status.md) - текущее состояние.
- [`../wiki/log.md`](../wiki/log.md) - журнал изменений.
- [`../wiki/outputs/`](../wiki/outputs/) - substantial generated outputs до writeback.
- [`../wiki/health/`](../wiki/health/) - health/lint reports.
- [`../wiki/people/`](../wiki/people/) - optional досье людей.
- [`../wiki/workflows/`](../wiki/workflows/) - повторяемые процессы.
- [`../wiki/decisions/`](../wiki/decisions/) - устойчивые решения.
- [`../CHANGELOG.md`](../CHANGELOG.md) - changelog шаблона.

## Source layer

- [`../raw/personal/`](../raw/personal/) - личные источники.
- [`../raw/personal/meetings/`](../raw/personal/meetings/) - optional личные meeting source-пакеты.
- [`../raw/work/`](../raw/work/) - рабочие источники.
- [`../raw/work/meetings/`](../raw/work/meetings/) - optional рабочие meeting source-пакеты.
- [`../raw/assets/`](../raw/assets/) - assets.

## AI layer

- [`../.ai/contract.md`](../.ai/contract.md) - общий контракт.
- [`../.ai/privacy.md`](../.ai/privacy.md) - правила приватности.
- [`../.ai/tool-profiles/codex.md`](../.ai/tool-profiles/codex.md) - профиль Codex.
- [`../.ai/tool-profiles/claude.md`](../.ai/tool-profiles/claude.md) - профиль Claude.

## Prompt layer

- [`../prompts/`](../prompts/) - reusable prompts для AI-чатов и тонких tool-specific оберток.
- [`../prompts/apply-template-upgrade.md`](../prompts/apply-template-upgrade.md) - merge-first upgrade prompt для уже персонализированных KB.

## Relationship layer

- [`meetings.md`](meetings.md) - optional индекс встреч.
- [`people-relations.md`](people-relations.md) - optional карта связей людей, организаций, проектов и встреч.

## Automation layer

- [`../scripts/`](../scripts/) - локальные проверки, Python wrapper, pre-commit installer и optional checked git sync.
