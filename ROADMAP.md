# Дорожная карта

`template-kb` должен оставаться lean: Markdown-first, переносимым между агентами
и полезным без hosted services.

## Ближайшие направления

- Добавить больше безопасных demo-сценариев для типовых KB workflows.
- Улучшить документацию по handoff-паттернам между Codex, Claude Code и Cursor.
- Расширить health reports более понятными manual review rubrics.

## Позже

- Optional GitHub issue/PR templates для команд, которым нужен OSS-style workflow.
- Больше golden-eval examples для повторяемых agent memory tasks.
- Optional CI examples, которые запускают `wiki_lint.py` без привязки к
  конкретной платформе.

## Не-цели

- Не требовать Obsidian plugins.
- Не добавлять hosted backend.
- Не управлять plaintext secrets.
- Не переносить domain-specific process из приватной KB.
