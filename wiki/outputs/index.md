# Индекс outputs

`wiki/outputs/` хранит существенные сгенерированные результаты, которые должны пережить чат, но еще не являются устойчивыми wiki-страницами.

## Назначение

- Сохранять переиспользуемые отчеты, сравнения, research briefs, матрицы и длинные ответы.
- Отделять рабочий результат сессии от устойчивого слоя `wiki/current-status.md`, `wiki/decisions/`, concept pages и project pages.
- Давать будущим агентам точку входа в уже выполненный анализ без повторного чтения всего source-контекста.

## Правила

- Имена output-файлов: `YYYY-MM-DD-short-slug.md`.
- Каждый output должен ссылаться на источники или явно маркировать неподтвержденные части как гипотезы.
- Для multi-source output добавляйте `Context Read`, если будущему агенту важно понимать реально прочитанный контекст.
- Output не заменяет writeback: устойчивые выводы переносятся через [`../workflows/writeback.md`](../workflows/writeback.md).
- Не переносите Secret-данные и лишние Sensitive-детали.
- Root `outputs/` не является knowledge layer и остается gitignored для локальных generated artifacts.

## Catalog

Пока нет сохраненных outputs.

## Связанные материалы

- [`../workflows/output.md`](../workflows/output.md)
- [`../workflows/query.md`](../workflows/query.md)
- [`../workflows/writeback.md`](../workflows/writeback.md)
