# Current Status

Date: YYYY-MM-DD (replace during setup)

## Текущее состояние

Факт: репозиторий создан из шаблона personal knowledge base.

Факт: шаблон содержит локальные проверки в `scripts/`: Python launcher, wiki lint, pre-commit installer и optional checked git sync.

Вывод: следующий шаг - персонализировать структуру под владельца, установить локальные проверки и добавить первый source-файл в `raw/personal/inbox/`.

Гипотеза: первые полезные сценарии будут связаны с личными проектами, рабочими заметками и планированием.

## Ближайшие действия

1. Заменить `YYYY-MM-DD` на текущую дату.
2. Уточнить назначение репозитория в `README.md`.
3. Добавить первую заметку в `raw/personal/inbox/`.
4. Установить pre-commit hook через `scripts/install_pre_commit.cmd` или прямой Python-запуск на macOS/Linux.
5. Попросить Codex разобрать заметку и предложить writeback.
6. Проверить `scripts/wiki_lint.cmd`, `git diff` и сделать первый commit.

## Открытые вопросы

- Какие 2-3 темы владелец хочет вести в этой базе?
- Какие данные нельзя отправлять в AI-сервисы?
- Нужно ли подключать Obsidian или достаточно Markdown + Git + Codex?

## Sources

- [`../README.md`](../README.md)
- [`../SETUP.md`](../SETUP.md)
- [`../raw/personal/inbox/first-note.example.md`](../raw/personal/inbox/first-note.example.md)
