# Wiki Index

`wiki/` - синтезированный слой памяти поверх `raw/`.

## Назначение

- Быстро восстановить текущий контекст.
- Хранить устойчивые выводы и решения.
- Показывать, какие источники важны.
- Помогать AI-агенту не начинать каждый раз с нуля.

## Основные страницы

- [`current-status.md`](current-status.md) - текущее состояние базы и ближайшие действия.
- [`log.md`](log.md) - журнал значимых изменений.
- [`schema.md`](schema.md) - правила создания wiki-страниц.
- [`outputs/`](outputs/) - substantial generated outputs до устойчивого writeback.
- [`health/`](health/) - датированные отчеты о качестве базы.
- [`people/`](people/) - optional досье людей и правила обновления контекста по людям.
- [`workflows/index.md`](workflows/index.md) - повторяемые процессы.
- [`decisions/index.md`](decisions/index.md) - устойчивые решения.

## Источники

- [`../raw/personal/`](../raw/personal/) - личные источники.
- [`../raw/work/`](../raw/work/) - рабочие источники.
- [`../raw/assets/`](../raw/assets/) - assets.
- [`../raw/personal/meetings/`](../raw/personal/meetings/) - optional личные meeting source-пакеты.
- [`../raw/work/meetings/`](../raw/work/meetings/) - optional рабочие meeting source-пакеты.

## Правило

`wiki/` не заменяет `raw/`. Если нужно знать, что было сказано или сохранено изначально, проверяйте source-файл в `raw/`.

Базовый цикл:

```text
source -> triage -> ingest/compile -> wiki -> query/output -> writeback -> lint/health
```

## Catalog

| Page | Type | Scope | Status | Summary | Sources |
|---|---|---|---|---|---|
| [`current-status.md`](current-status.md) | status | repo | draft | Текущее состояние базы и ближайшие действия после создания из шаблона. | `README.md`, `raw/personal/inbox/first-note.example.md` |
| [`log.md`](log.md) | log | repo | active | Журнал значимых изменений контекста. | current session |
| [`schema.md`](schema.md) | schema | repo | active | Минимальные типы wiki-страниц и правила качества. | `wiki/` |
| [`outputs/index.md`](outputs/index.md) | index | repo | active | Каталог substantial generated outputs, которые должны пережить чат до writeback. | `wiki/workflows/output.md` |
| [`health/index.md`](health/index.md) | index | repo | active | Каталог dated health/lint reports по состоянию базы. | `wiki/workflows/lint.md`, `scripts/wiki_lint.py` |
| [`people/index.md`](people/index.md) | index | repo | optional | Optional досье людей и правила обновления контекста по людям. | `wiki/workflows/meeting-ingest.md` |
| [`workflows/index.md`](workflows/index.md) | index | repo | active | Каталог повторяемых процессов работы с базой. | `wiki/workflows/` |
| [`decisions/index.md`](decisions/index.md) | index | repo | active | Каталог устойчивых решений. | `wiki/decisions/` |
