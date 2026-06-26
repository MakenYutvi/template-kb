Роль

Ты помогаешь провести еженедельный maintenance review личной базы знаний.

Вход

- Путь к репозиторию или текущий workspace.
- Optional focus area: personal, work, projects, decisions, sources.

Результат

Создай короткий weekly review report и обновляй `wiki/` только если изменился
durable context.

Процесс

1. Прочитай `AGENTS.md`, `README.md`, `wiki/index.md`, `wiki/current-status.md`, `wiki/log.md` и `indexes/map.md`.
2. Проверь последние Git-изменения и последние записи `wiki/log.md`.
3. Найди:
   - открытые вопросы;
   - устаревшие next actions;
   - source-области без wiki summaries;
   - wiki-страницы, которым может быть нужна compaction;
   - решения, которые стоит задокументировать;
   - пропущенные обновления index или manifest.
4. Запусти доступные проверки:
   - `scripts/kb_doctor.cmd` на Windows, если доступен;
   - `scripts/wiki_lint.cmd` на Windows, если доступен;
   - Python equivalents на macOS/Linux.
5. Рекомендуй не больше 5 next actions.
6. Если review сам создает durable context, обнови `wiki/current-status.md` и `wiki/log.md`.

Формат результата

1. Текущее состояние.
2. Findings.
3. Top 5 next actions.
4. Suggested writeback.
5. Checks run.
6. Уверенность и ограничения.

Правила

- Не читай весь `raw/` без понятной причины.
- Не выноси sensitive details в broad wiki pages.
- Помечай uncertain claims как гипотезы.
