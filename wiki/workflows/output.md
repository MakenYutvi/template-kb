# Workflow output

Используй этот workflow, когда ответ, отчет или анализ должен пережить текущий чат, но еще не должен становиться устойчивой concept/project/status/decision страницей.

## Цель

Сохранить substantial generated output в `wiki/outputs/` как проверяемый рабочий результат, не подменяя им source layer и не раздувая устойчивую wiki-память.

## Когда использовать

- Ответ длинный, многошаговый или содержит reusable analysis.
- Результат нужен как отчет, comparison matrix, research brief, gap analysis, reading plan или decision-support note.
- Выводы могут быть полезны позднее, но еще требуют review перед переносом в `wiki/current-status.md`, concept/project pages или `wiki/decisions/`.

## Когда не использовать

- Результат одноразовый и не имеет долгосрочной ценности.
- Есть уже принятое устойчивое решение: тогда используй `wiki/decisions/`.
- Нужно обновить текущий статус проекта или процесса: тогда используй `wiki/workflows/writeback.md`.
- Output содержал бы Secret-данные или лишние Sensitive-детали.

## Формат

Файл: `wiki/outputs/YYYY-MM-DD-short-slug.md`.

Минимальные секции:

- Context.
- Sources.
- Result.
- Durable Findings.
- Follow-up.

Опциональная секция для substantial multi-source outputs:

- Context Read.

`Context Read` фиксирует, что агент реально прочитал или проверил перед выводом:

- Local Sources.
- External Sources.
- Tools/Commands.
- Limits.

Не сохраняй полный transcript, raw tool dump или Sensitive детали. Достаточно перечислить существенные файлы, URL, команды и ограничения анализа.

## Шаги

1. Проверь, достаточно ли `wiki/log.md` или нужен отдельный output.
2. Определи класс данных: Public, Personal, Work, Sensitive или Secret.
3. Создай output с кратким контекстом, источниками, результатом и follow-up.
4. Для multi-source анализа добавь `Context Read`, если без него будущий агент не поймет, на чем основан вывод.
5. Добавь файл в `wiki/outputs/index.md`.
6. Если появились устойчивые выводы, выполни `wiki/workflows/writeback.md`.
7. Если output важен для будущих сессий, добавь краткую запись в `wiki/log.md`.

## Критерий готовности

- Output можно найти через `wiki/outputs/index.md`.
- Источники указаны или неопределенность явно помечена.
- Для substantial multi-source output есть `Context Read` или понятная причина, почему он не нужен.
- Durable findings либо перенесены через writeback, либо явно оставлены как follow-up.
- Sensitive/Secret-риски проверены.
