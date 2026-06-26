# Журнал изменений

## 2026-06-26 - Upgrade template-kb memory workflows and presentation

Этот release упаковывает `template-kb` как Markdown-first систему памяти для
AI-агентов: source provenance, durable outputs, writeback workflows, health
checks, безопасный upgrade существующих KB и более взрослая публичная витрина
репозитория.

Главный lifecycle теперь явно описан во всех core docs:

```text
source -> triage -> ingest/compile -> wiki -> query/output -> writeback -> lint/health
```

Ценность изменения в том, что KB перестает быть просто папкой заметок. У нее
появляется проверяемая операционная модель: где лежат источники, где живут
выводы, как сохранять важные generated outputs, как проверять качество памяти и
как обновлять уже персонализированные базы без перезаписи пользовательской
работы.

### Добавлено

- `wiki/outputs/` для substantial generated outputs до durable writeback.
- `wiki/health/` для dated lint/health reports и manual quality review.
- Workflows: `output`, `golden-eval`, `meeting-ingest`, расширенные
  `writeback`, `source-provenance` и `lint`.
- Практики `Context Read`, `Reference Mirror -> Overlay`, `Feedback Proposal` и
  manual health rubric.
- Optional people/meetings starter pack: `wiki/people/`,
  `indexes/meetings.md`, `indexes/people-relations.md`,
  `raw/personal/meetings/`, `raw/work/meetings/`.
- `prompts/apply-template-upgrade.md` как canonical versioned upgrade prompt.
- `scripts/prune_os_scripts.py` и Windows wrappers для удаления script wrappers,
  которые не относятся к текущей operating system после setup/upgrade
  personalized KB.
- `new_kb_item` skeletons для `output`, `health`, `person` и расширенный
  `meeting` skeleton.
- Product maturity files: `LICENSE`, `SECURITY.md`, `ROADMAP.md`.
- `docs/demo-walkthrough.md` с безопасным end-to-end примером memory flow.

### Изменено

- `README.md` стал публичной витриной проекта: problem statement, memory
  lifecycle diagram, value table, entrypoints для новой KB, upgrade и local
  checks.
- `SETUP.md`, `AGENTS.md`, `.ai/contract.md`, `wiki/index.md`,
  `wiki/schema.md` и workflow docs приведены к новой memory model.
- Markdown-документация переведена на русский как основной публичный язык;
  technical identifiers, commands, filenames и устойчивые workflow terms
  сохранены там, где они являются интерфейсом.
- `prompts/apply-template-upgrade.md` теперь `Prompt Version: 2026-06-26.1`.
  Служебная информация перенесена в конец, а запуск upgrade prompt рекомендован
  в planning mode перед применением изменений.
- `prompts/README.md` описывает versioned upgrade prompt как зрелый public
  interface.
- `wiki_lint.py` проверяет output/health naming, Markdown links, catalog и
  manifest expectations без private repo-specific required paths.
- `kb_doctor.py` ожидает public maturity files, demo walkthrough и корректно
  учитывает OS-pruned repositories.
- `README.md` кратко описывает local helpers, а подробные команды оставлены в
  `SETUP.md`.

### Заметки по миграции

Для существующих KB repositories делайте upgrade через canonical prompt, а не
копированием нового template поверх старого repository.

Рекомендуемый flow:

1. Скопируйте
   [`prompts/apply-template-upgrade.md`](https://github.com/MakenYutvi/template-kb/blob/main/prompts/apply-template-upgrade.md).
2. Вставьте prompt в агента, запущенного внутри существующей personalized KB.
3. Лучше запускать prompt в planning mode: сначала получить merge plan, риски и
   список затронутых файлов, затем разрешить применение изменений.

Агент должен применить upgrade merge-first: добавить новые universal workflows и
starter sections, аккуратно обновить shared docs/scripts и сохранить existing
`raw/`, personalized `wiki/`, indexes, decisions, prompts и local conventions.

Не заменяйте `wiki/current-status.md`, `wiki/log.md` или
`manifests/sources.md` wholesale в personalized KB. Агент должен сообщить
использованные `Prompt Version` и template commit/tag, если они доступны.

### Совместимость

- Upgrade остается Markdown-first и Obsidian-compatible без требования
  `.obsidian/` или plugins.
- Public `template-kb` остается cross-platform и хранит Windows/macOS/Linux
  script paths.
- Personalized KB repositories могут запускать `prune_os_scripts` после setup
  или upgrade, если не нужна одна KB для нескольких operating systems.
- Commit и push остаются explicit user actions, а не automatic setup steps.

### Проверка

Release проверен на starter repo:

- `.\scripts\wiki_lint.cmd`
- `.\scripts\kb_doctor.cmd`
- `git diff --check`
- Python bytecode compilation для updated scripts
- `new_kb_item.py` dry-runs для `output`, `health`, `person` и `meeting`
- repository scan на private/domain-specific traces перед release
