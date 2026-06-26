# Workflow source provenance

Этот workflow определяет, как связывать wiki-утверждения с источниками.

## Принцип

Source имеет приоритет над summary. `wiki/` помогает быстро восстановить контекст, но не является единственным источником истины.

## Уровни утверждений

- Source-backed fact: утверждение подтверждено конкретным source-файлом.
- Decision-backed fact: утверждение подтверждено decision log.
- Inference: логический вывод из source-backed facts.
- Hypothesis: предположение без достаточного подтверждения.

## Как ссылаться на источники

Используй обычные Markdown-ссылки:

```markdown
- `raw/work/example-project/source-note.md`
```

Для нескольких источников добавляй секцию:

```markdown
## Sources

- `path/to/source.md`
- `wiki/decisions/YYYY-MM-DD-title.md`
```

## Когда не переносить детали в wiki

- Source содержит секреты, доступы, ключи, токены или приватные конфигурации.
- Source содержит персональные, финансовые, юридические или чувствительные рабочие детали.
- Достаточно ссылки на source и короткого безопасного summary.

## Когда нужно перепроверять source

- Перед изменением рабочего процесса или документа.
- Перед использованием точных чисел, дат, имен, статусов, юридических формулировок.
- Если wiki-страница старше релевантного source.
- Если пользователь указывает, что контекст мог измениться.
- Если `scripts/wiki_lint.py` сообщает `source-digest` или `staged-source-drift`.

## Digest tracking

Для источников, которые уже reviewed/writeback в `wiki/` и должны оставаться синхронизированными, добавляй opt-in запись в [`../../manifests/source-digests.json`](../../manifests/source-digests.json).

Правило:

- `path` указывает на файл или директорию внутри репозитория.
- `kind` равен `file` или `tree`.
- `sha256` обновляется только после проверки source и соответствующих wiki-summary.
- Не добавляй чувствительные source в digest manifest, если сам путь или факт отслеживания раскрывает лишнюю информацию.

## Конфликт wiki и source

Если `wiki/` противоречит source:

1. Считай source более надежным.
2. Отметь конфликт в ответе или рабочей заметке.
3. Обнови wiki через `writeback.md`, если это в рамках задачи.

## Reference Mirror и Overlay

`Reference Mirror` - локальное read-only/refreshable зеркало внешней системы или выгрузки. Примеры: exported docs, issue tracker export, spreadsheet dump, mailbox export.

Правила:

- Не считай reference mirror автоматически source of truth, если в README/frontmatter указана ограниченная freshness или mirror status.
- Не редактируй mirror ради summary; обновляй его только штатным pull/export workflow.
- Сохраняй синтезированные выводы отдельно: в `wiki/`, `wiki/outputs/`, source note или decision log.

`Overlay` - синтезированный слой поверх reference mirror: проверенные выводы, решения, связи, TODO или corrections.

Правила:

- Overlay должен ссылаться на mirror/source и явно отделять факты от выводов.
- Если mirror обновился и противоречит overlay, перепроверь source и обнови overlay через `writeback.md`.
- Не превращай overlay в копию внешнего документа.
