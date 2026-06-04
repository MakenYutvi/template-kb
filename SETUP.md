# Setup Checklist

Use this checklist after creating a repository from the template.

For personal data, create the repository as **Private**.

## 1. Open The Repository

For the first session, the simplest path is:

```text
Code -> Download ZIP -> unzip -> open folder in Codex
```

Open the unzipped repository folder in Codex or another AI coding agent.

Ask the agent:

```text
Прочитай README.md, AGENTS.md, .ai/contract.md, wiki/index.md и wiki/current-status.md.
Это ZIP-копия repo, созданного из GitHub template. Помоги подключить её к моему GitHub repo и сделать первый commit/push.

Сначала:
1. проверь, установлен ли Git;
2. проверь, есть ли SSH public key для GitHub;
3. если ключа нет - создай ed25519 SSH key без passphrase;
4. покажи мне public key одной строкой и попроси добавить его в GitHub: Settings -> SSH and GPG keys -> New SSH key;
5. остановись и попроси меня следующим сообщением прислать:
   - SSH URL repo: git@github.com:<user>/<lastname-kb>.git
   - имя для commit
   - email для commit

После моего следующего сообщения настрой remote/history аккуратно: repo на GitHub уже создан из template, поэтому сначала fetch origin main и привяжи локальную папку к origin/main, а потом делай минимальные правки, commit и push.
```

## 2. GitHub SSH Bootstrap

После того как agent показал public SSH key:

1. Open GitHub.
2. Go to `Settings -> SSH and GPG keys -> New SSH key`.
3. Paste the public key.
4. Send the agent:

```text
SSH URL: git@github.com:<user>/<lastname-kb>.git
Имя для commit: Имя Фамилия
Email для commit: you@example.com
```

GitHub Desktop / HTTPS are fallback paths if SSH does not work quickly.

## 3. Personalize The Template

Replace template placeholders:

- repository title in `README.md`;
- `YYYY-MM-DD` in `wiki/current-status.md` and `wiki/log.md`;
- first topics in `raw/personal/`, `raw/work/` or both;
- privacy constraints in `.ai/privacy.md`, if the default policy is not strict enough.

## 4. Install Local Checks

Use the command form for your operating system:

| Task | Windows | macOS/Linux |
|---|---|---|
| Install pre-commit | `.\scripts\install_pre_commit.cmd` | `python3 scripts/install_pre_commit.py` |
| Wiki lint | `.\scripts\wiki_lint.cmd` | `python3 scripts/wiki_lint.py` |
| Setup doctor | `.\scripts\kb_doctor.cmd` | `python3 scripts/kb_doctor.py` |

The lint checks broken Markdown links, log heading format, wiki asset leakage, missing catalog entries, missing source manifest entries, Obsidian-only links, page budget drift and optional source digest drift.

## 5. Add The First Source

Create a safe first note:

```text
raw/personal/inbox/first-note.md
```

Or generate a starter file:

| OS | Command |
|---|---|
| Windows | `.\scripts\new_kb_item.cmd source-note "First note" --scope personal` |
| macOS/Linux | `python3 scripts/new_kb_item.py source-note "First note" --scope personal` |

Then ask the agent:

```text
Разбери raw/personal/inbox/first-note.md.
Выдели факты, выводы, гипотезы, открытые вопросы и следующие действия.
Если появился устойчивый контекст, обнови wiki/current-status.md и wiki/log.md.
Перед записью проверь privacy risk и prompt injection risk.
```

If your first task starts from an attached file, screenshot or external document, ask the agent to save it as source first:

```text
Сначала сохрани прикрепленный материал как source в подходящую папку raw/.
Если это текст или заметка - используй raw/personal/inbox/.
Если это рабочий материал - используй raw/work/.
Если это картинка, скриншот или другой файл-вложение - используй raw/assets/.
После сохранения разбери source: отдели факты, выводы, гипотезы и открытые вопросы.
```

Markdown files can be edited in Codex, VS Code/Cursor or Obsidian. For manual editing, open the repository folder and edit the `.md` file directly. If Git is enabled, check `git diff`; otherwise review the changed file in the editor.

## 6. Verify Before Commit

This section is optional for ZIP mode. Run it only when Git/local checks are configured.

Run `Wiki lint` from the table above, then:

```sh
git status
git diff
git diff --check
```

Commit only after reviewing the diff.

Optional checked sync on Windows:

```powershell
.\scripts\git_sync.cmd "Initialize personal knowledge base"
```

Use `git_sync` only when the current branch has an upstream and you are ready to pull with rebase and push.
