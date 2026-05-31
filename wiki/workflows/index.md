# Workflows

Повторяемые процессы работы с knowledge base.

## Основные workflows

- [`query.md`](query.md) - ответить из накопленного контекста.
- [`ingest.md`](ingest.md) - добавить новый source и разобрать его.
- [`writeback.md`](writeback.md) - сохранить устойчивый результат сессии.

## Базовый цикл

```text
source -> triage -> ingest -> wiki -> query -> writeback
```
