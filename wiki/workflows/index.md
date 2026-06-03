# Workflows

Повторяемые процессы работы с knowledge base.

## Основные workflows

- [`query.md`](query.md) - ответить из накопленного контекста.
- [`triage.md`](triage.md) - проверить proposed writes перед крупным ingest или структурной правкой.
- [`ingest.md`](ingest.md) - добавить новый source и разобрать его.
- [`writeback.md`](writeback.md) - сохранить устойчивый результат сессии.
- [`lint.md`](lint.md) - проверить качество wiki и запустить автоматический lint.
- [`source-provenance.md`](source-provenance.md) - проверить связь wiki-утверждений с источниками.
- [`context-budget.md`](context-budget.md) - выбрать минимальный достаточный контекст.
- [`assets.md`](assets.md) - сохранить изображения, скриншоты и вложения в source-слое.

## Базовый цикл

```text
source -> triage -> ingest -> wiki -> query -> writeback -> lint
```
