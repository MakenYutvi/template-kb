# Workflow wiki lint

Используй этот workflow периодически или перед крупными изменениями структуры базы знаний.

## Цель

Найти расхождения, устаревание, сиротские страницы и слабые места в `wiki/`.

## Проверки

1. Orphan pages: страницы без входящих или исходящих ссылок.
2. Missing sources: важные утверждения без source или decision.
3. Stale pages: страницы с устаревшим статусом, датами или next actions.
4. Contradictions: противоречия между `wiki/` и source-файлами.
5. Duplicate concepts: несколько страниц об одном и том же без причины.
6. Missing cross-links: связанные темы не ссылаются друг на друга.
7. Privacy leakage: sensitive или secret детали вынесены в summary.
8. Broken links: Markdown-ссылки указывают на несуществующие файлы.
9. Missing catalog entries: wiki-страницы отсутствуют в `wiki/index.md` Catalog.
10. Missing manifest entries: устойчивые source-области отсутствуют в `manifests/sources.md`.
11. Stale source references: wiki ссылается на source, который был существенно обновлен после review.
12. Log format drift: новые записи `wiki/log.md` не используют heading `YYYY-MM-DD | kind | short-title`.
13. Asset leakage: изображения, вложения или web assets сохранены в `wiki/` вместо source-слоя.
14. Page budget drift: wiki-страницы становятся слишком длинными и требуют compaction/split.
15. Source digest drift: opt-in источники в `manifests/source-digests.json` изменились после review.
16. Output/health naming: tracked outputs и health reports используют согласованные имена и имеют index.
17. Manual health rubric: source grounding, contradiction absence, novelty/redundancy, disambiguation, context preservation, link/index coverage и privacy leakage проверены вручную, если scope проверки значимый.

## Ручная проверка

- Просмотреть `wiki/index.md`, `wiki/current-status.md`, `wiki/decisions/index.md`.
- Просмотреть `manifests/sources.md`.
- Проверить последние записи `wiki/log.md`.
- Сравнить 2-3 важных wiki-summary с исходниками.
- Для значимых проверок пройти ручную rubric: source grounding, contradiction absence, novelty/redundancy, disambiguation, context preservation, link/index coverage, privacy leakage.
- Проверить, что `.obsidian/` не попал в git.
- Проверить, что значимые assets лежат в `raw/assets/`, `raw/work/` или `raw/personal/`, а не в `wiki/`.

## Автоматическая проверка

Сначала запускай lightweight lint:

```powershell
.\scripts\wiki_lint.cmd
```

Не запускай `python scripts/wiki_lint.py` напрямую в Windows-сессиях агентов: `python` часто отсутствует в PATH. Если Windows wrappers есть, используй `.cmd` wrapper, чтобы не зависеть от PowerShell ExecutionPolicy. Wrapper `scripts/wiki_lint.cmd` использует `scripts/kb_python.ps1`, который ищет `KB_PYTHON`, repo virtualenv, bundled Python Codex, затем системные `python`/`python3`/`py -3`.

На macOS/Linux или в KB, где Windows wrappers удалены через OS pruning, используй:

```sh
python3 scripts/wiki_lint.py
```

Скрипт покрывает объективные проверки: broken links, log format, устаревшие root source paths, старый цикл, asset leakage, catalog entries, manifest entries, Obsidian-only links, output/health naming, page budget, opt-in source digests и staged source drift warning.

Чтобы запускать lint автоматически перед `git commit`, установи локальный hook:

```powershell
.\scripts\install_pre_commit.cmd
```

На macOS/Linux или после pruning используй:

```sh
python3 scripts/install_pre_commit.py
```

Installer сохраняет существующий `.git/hooks/pre-commit.ps1` как `.git/hooks/pre-commit.local.ps1`, если он не был сгенерирован template-kb installer.

Page budget и staged source drift могут выдавать warning. Warning не блокирует commit, но должен быть разобран в рамках writeback/no-op.

Ручные проверки все еще нужны для противоречий, privacy leakage и качества summaries.

## Результат

После значимой lint/health-сессии создай отчет `wiki/health/YYYY-MM-DD-health.md` или `wiki/health/YYYY-MM-DD-health-<scope>.md`:

```text
# YYYY-MM-DD Health Report

## Scope

## Checks

## Rubric

## Findings

## Fixed

## Follow-up
```

После lint-сессии также обнови `wiki/log.md`, если результат должен быть виден будущим сессиям:

```text
## YYYY-MM-DD | lint | short-title

- Scope:
- Findings:
- Fixed:
- Follow-up:
```

Если найдено важное архитектурное решение, добавь decision log.
