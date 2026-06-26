# Индекс health reports

`wiki/health/` хранит датированные отчеты о состоянии базы знаний: lint-сессии, ручные аудиты, проверки устаревания, слабых связей и качества writeback.

## Назначение

- Фиксировать результат значимых проверок качества KB как проверяемый артефакт.
- Отделять подробный health report от краткой записи в `wiki/log.md`.
- Сохранять follow-up по broken links, stale pages, duplicate concepts, source drift, privacy leakage и missing cross-links.

## Правила

- Имена отчетов: `YYYY-MM-DD-health.md` или `YYYY-MM-DD-health-<scope>.md`.
- Каждый отчет должен содержать scope, checks, rubric, findings, fixed и follow-up.
- Автоматический `scripts/wiki_lint.py` покрывает только объективные проверки; противоречия, duplicate concepts и privacy leakage требуют ручного review.
- Если health-сессия меняет структуру, процесс или важный контекст, краткий итог также добавляется в `wiki/log.md`.

## Catalog

Пока нет сохраненных health reports.

## Связанные материалы

- [`../workflows/lint.md`](../workflows/lint.md)
- [`../workflows/source-provenance.md`](../workflows/source-provenance.md)
- [`../../scripts/wiki_lint.py`](../../scripts/wiki_lint.py)
