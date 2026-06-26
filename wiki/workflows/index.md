# Workflows

Повторяемые процессы работы с knowledge base.

## Основные workflows

- [`query.md`](query.md) - ответить из накопленного контекста.
- [`triage.md`](triage.md) - проверить proposed writes перед крупным ingest или структурной правкой.
- [`ingest.md`](ingest.md) - добавить новый source, разобрать его и выполнить compile в wiki/index при необходимости.
- [`output.md`](output.md) - сохранить substantial generated output перед устойчивым writeback.
- [`writeback.md`](writeback.md) - сохранить устойчивый результат сессии.
- [`lint.md`](lint.md) - проверить качество wiki, запустить автоматический lint и при необходимости сохранить health report.
- [`source-provenance.md`](source-provenance.md) - проверить связь wiki-утверждений с источниками.
- [`golden-eval.md`](golden-eval.md) - ручная регрессионная проверка повторяемых KB-задач.
- [`context-budget.md`](context-budget.md) - выбрать минимальный достаточный контекст.
- [`assets.md`](assets.md) - сохранить изображения, скриншоты и вложения в source-слое.
- [`meeting-ingest.md`](meeting-ingest.md) - optional обработка транскрипций встреч, summary и writeback контекста по людям.

## Базовый цикл

```text
source -> triage -> ingest/compile -> wiki -> query/output -> writeback -> lint/health
```
