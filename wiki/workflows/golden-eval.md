# Workflow golden eval

Используй этот workflow, когда повторяемый KB-процесс нужно проверить на регрессию по заранее ожидаемым фактам, ссылкам и safety-ограничениям.

## Цель

Сделать ручную регрессионную проверку для задач, где качество результата можно оценить по устойчивому набору expected facts, must-preserve facts и forbidden leakage.

В v1 golden eval остается docs-only практикой: отдельный `wiki/goldens/` не создается, runner не добавляется, semantic lint не вводится.

## Когда использовать

- Meeting ingest, если повторяется один и тот же тип транскриптов и summary.
- People-card updates, если карточки людей обновляются из похожих source packs.
- Recurring project summaries, если отчет или анализ регулярно строится по сходным входам.
- Source-provenance checks, если нужно убедиться, что wiki-summary не оторвалась от источника.

## Формат case

Фиксируй case в relevant output, health report или source workflow note.

```text
## Golden Case: short-title

Scope:
Input Sources:
Expected Facts:
Must Preserve:
Forbidden Leakage:
Expected Links:
Tool Expectations:
Result:
```

Поля:

- `Scope`: какой workflow или доменная область проверяется.
- `Input Sources`: конкретные source-файлы, output или wiki-страницы.
- `Expected Facts`: атомарные проверяемые факты, которые должны попасть в результат.
- `Must Preserve`: уже существующие факты/решения, которые нельзя потерять или исказить.
- `Forbidden Leakage`: Secret/Sensitive детали, которые нельзя переносить в summary.
- `Expected Links`: ссылки, которые должны быть сохранены или добавлены.
- `Tool Expectations`: если важно, какие источники или команды должны/не должны использоваться.
- `Result`: pass/fail, дата проверки, краткая причина и follow-up.

## Ручная проверка

1. Выбери минимальный case, который реально защищает от повторной ошибки.
2. Сверь результат с `Expected Facts`, `Must Preserve` и `Forbidden Leakage`.
3. Проверь ссылки и provenance по `wiki/workflows/source-provenance.md`.
4. Зафиксируй результат в output, health report или log, если проверка существенная.
5. Если один и тот же case повторился 3+ раза, вернись к вопросу об отдельном каталоге или автоматизации.

## Критерий готовности

- Case привязан к конкретным input sources.
- Expected facts атомарны и проверяемы.
- Sensitive/Secret leakage проверен явно.
- Result содержит pass/fail и follow-up.
- Не создан новый обязательный каталог и не добавлен runner без отдельного решения.
