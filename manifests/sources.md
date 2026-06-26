# Манифест источников

Основные source-области репозитория.

## Правила обновления

- Обновляйте manifest, когда появляется новая устойчивая source-область.
- Не добавляйте сюда каждый мелкий файл.
- Для чувствительных источников указывайте только безопасное описание.
- Если нужен точный checksum файла или дерева, добавляйте opt-in запись в [`source-digests.json`](source-digests.json).

| Source path | Type | Scope | Privacy | Linked wiki | Notes |
|---|---|---|---|---|---|
| `raw/personal/` | markdown/files | personal | personal | `wiki/current-status.md` | Личные заметки, проекты и inbox. |
| `raw/personal/meetings/` | markdown/files | personal | sensitive | `wiki/workflows/meeting-ingest.md`, `wiki/people/index.md`, `indexes/meetings.md` | Optional личные meeting source-пакеты: транскрипты, summary и writeback candidates. |
| `raw/work/` | markdown/files | work | work | `wiki/current-status.md` | Рабочие заметки и документы без секретов. |
| `raw/work/meetings/` | markdown/files | work | work | `wiki/workflows/meeting-ingest.md`, `wiki/people/index.md`, `indexes/meetings.md` | Optional рабочие meeting source-пакеты: транскрипты, summary и writeback candidates. |
| `raw/assets/` | files | mixed | depends | `indexes/map.md` | Скриншоты, вложения, изображения. |
| `wiki/` | markdown | mixed | derived | `wiki/index.md` | Синтезированный слой памяти. |
| `wiki/outputs/` | markdown | repo | derived | `wiki/outputs/index.md` | Substantial generated outputs до устойчивого writeback. |
| `wiki/health/` | markdown | repo | derived | `wiki/health/index.md` | Датированные lint/health reports и ручные quality checks. |
| `wiki/people/` | markdown | mixed | derived | `wiki/people/index.md` | Optional досье людей как synthesis layer с provenance. |
| `indexes/` | markdown | mixed | derived | `indexes/map.md` | Навигационные карты. |
| `prompts/` | markdown | repo | public | `indexes/map.md` | Reusable tool-neutral AI prompts. |
| `scripts/` | scripts | repo | public | `wiki/workflows/lint.md`, `SETUP.md` | Локальные проверки, Python wrapper, pre-commit installer, setup doctor, item generator, digest manager и optional checked git sync. |
