# Промпты

Reusable prompts - это шаблоны задач, которые можно копировать в AI-чат или
оборачивать tool-specific command.

Эта папка tool-neutral: промпты не должны зависеть от Codex, Cursor, Claude Code
или конкретного локального пути. Repository-specific paths, project names,
people и constraints подставляются во вход при использовании шаблона.

## Формат

Каждый prompt file должен содержать executable instruction. Для обычных
copy-paste prompts избегайте frontmatter, `# name`, `# description` и wrapper
comments. Имя prompt задается именем файла; назначение описано в каталоге ниже.

Long-lived operational prompts, например migration prompts, могут включать
in-body version block, если пользователям важно знать, какое поведение они
скопировали. Version block должен быть human-readable и входить в копируемый
prompt.

Рекомендуемые секции:

- `Роль` - кем должна действовать модель.
- `Вход` - что должен предоставить пользователь.
- `Результат` - ожидаемый результат и структура.
- `Процесс` - упорядоченные шаги, если задача этого требует.
- `Prompt Version` и `Prompt Changelog` - только для long-lived operational prompts с versioned behavior.

Имена файлов должны использовать `kebab-case.md`.

## Каталог

| Prompt | Назначение |
|---|---|
| [`setup-new-kb.md`](setup-new-kb.md) | Промпт для персонализации нового репозитория, созданного из этого шаблона. |
| [`apply-template-upgrade.md`](apply-template-upgrade.md) | Canonical versioned upgrade interface для аккуратной миграции существующей personalized KB по более новому template без перезаписи user work. |
| [`create-kb-helper-script.md`](create-kb-helper-script.md) | Промпт для добавления небольшого local helper script с wrappers, docs и verification. |
| [`ingest-source.md`](ingest-source.md) | Промпт для ingest одного нового source-файла в durable wiki memory. |
| [`review-kb-diff.md`](review-kb-diff.md) | Промпт для review repository diff перед commit. |
| [`weekly-review.md`](weekly-review.md) | Промпт для periodic maintenance review базы знаний. |
| [`web-chat-to-kb-transfer.md`](web-chat-to-kb-transfer.md) | Короткий copy-paste prompt для подготовки transfer package из текущего web GPT chat. |
| [`web-gpt-global-context-to-kb-transfer.md`](web-gpt-global-context-to-kb-transfer.md) | Короткий copy-paste prompt для подготовки transfer package из global web GPT context. |

## Быстрый старт для transfer prompts

По умолчанию копируйте основной compact prompt прямо в web GPT:

```powershell
Get-Content -Raw -Encoding UTF8 -LiteralPath .\prompts\web-chat-to-kb-transfer.md | Set-Clipboard
```

Для global context:

```powershell
Get-Content -Raw -Encoding UTF8 -LiteralPath .\prompts\web-gpt-global-context-to-kb-transfer.md | Set-Clipboard
```

Web GPT должен выдать два блока: `КОРОТКАЯ КОМАНДА ДЛЯ CODEX` и
`TRANSFER PAYLOAD`. В Codex сначала отправьте короткую команду, затем payload
или `.txt` файл с payload вторым сообщением.
