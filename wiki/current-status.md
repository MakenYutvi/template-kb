# Текущий статус

Date: YYYY-MM-DD (замените при настройке)

## Текущее состояние

Факт: репозиторий создан из шаблона personal knowledge base.

Факт: шаблон содержит локальные проверки и helpers в `scripts/`: Python launcher, wiki lint, pre-commit installer, setup doctor, item generator, digest manager, OS script pruning и optional checked git sync.

Факт: шаблон содержит tracked-разделы `wiki/outputs/` и `wiki/health/`, optional people/meetings starter pack и workflow `source -> triage -> ingest/compile -> wiki -> query/output -> writeback -> lint/health`.

Вывод: следующий шаг - персонализировать структуру под владельца, установить локальные проверки и добавить первый source-файл в `raw/personal/inbox/`.

Гипотеза: первые полезные сценарии будут связаны с личными проектами, рабочими заметками и планированием.

## Ближайшие действия

1. Заменить `YYYY-MM-DD` на текущую дату.
2. Уточнить назначение репозитория в `README.md`.
3. Добавить первую заметку в `raw/personal/inbox/`.
4. Установить pre-commit hook через `scripts/install_pre_commit.cmd` или прямой Python-запуск на macOS/Linux.
5. После настройки локальных проверок удалить wrappers для другой ОС через `scripts/prune_os_scripts.py`, если KB не должна оставаться cross-platform.
6. Попросить Codex разобрать заметку и предложить writeback.
7. При необходимости использовать `wiki/outputs/` для длинных отчетов или `wiki/people/`/meeting workflow для устойчивого контекста по людям.
8. Проверить wiki lint, `git diff` и сделать первый commit.

## Открытые вопросы

- Какие 2-3 темы владелец хочет вести в этой базе?
- Какие данные нельзя отправлять в AI-сервисы?
- Нужно ли подключать Obsidian или достаточно Markdown + Git + Codex/Claude?

## Sources

- [`../README.md`](../README.md)
- [`../SETUP.md`](../SETUP.md)
- [`../raw/personal/inbox/first-note.example.md`](../raw/personal/inbox/first-note.example.md)
