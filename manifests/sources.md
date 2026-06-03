# Source Manifest

Основные source-области репозитория.

## Правила обновления

- Обновляйте manifest, когда появляется новая устойчивая source-область.
- Не добавляйте сюда каждый мелкий файл.
- Для чувствительных источников указывайте только безопасное описание.
- Если нужен точный checksum файла или дерева, добавляйте opt-in запись в [`source-digests.json`](source-digests.json).

| Source path | Type | Scope | Privacy | Linked wiki | Notes |
|---|---|---|---|---|---|
| `raw/personal/` | markdown/files | personal | personal | `wiki/current-status.md` | Личные заметки, проекты и inbox. |
| `raw/work/` | markdown/files | work | work | `wiki/current-status.md` | Рабочие заметки и документы без секретов. |
| `raw/assets/` | files | mixed | depends | `indexes/map.md` | Скриншоты, вложения, изображения. |
| `wiki/` | markdown | mixed | derived | `wiki/index.md` | Синтезированный слой памяти. |
| `indexes/` | markdown | mixed | derived | `indexes/map.md` | Навигационные карты. |
| `prompts/` | markdown | repo | public | `indexes/map.md` | Reusable tool-neutral AI prompts. |
| `scripts/` | scripts | repo | public | `wiki/workflows/lint.md`, `SETUP.md` | Локальные проверки, Python wrapper, pre-commit installer и optional checked git sync. |
