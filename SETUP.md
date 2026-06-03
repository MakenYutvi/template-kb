# Setup Checklist

Use this checklist after creating a repository from the template.

## 1. Open The Repository

Open the repository folder in Codex or another AI coding agent.

Ask the agent:

```text
Прочитай README.md, AGENTS.md, .ai/contract.md, wiki/index.md и wiki/current-status.md.
Помоги персонализировать этот knowledge base repository.
Сначала проверь текущие файлы и git status, затем предложи минимальные правки.
```

## 2. Personalize The Template

Replace template placeholders:

- repository title in `README.md`;
- `YYYY-MM-DD` in `wiki/current-status.md` and `wiki/log.md`;
- first topics in `raw/personal/`, `raw/work/` or both;
- privacy constraints in `.ai/privacy.md`, if the default policy is not strict enough.

## 3. Install Local Checks

On Windows:

```powershell
.\scripts\install_pre_commit.cmd
.\scripts\wiki_lint.cmd
.\scripts\kb_doctor.cmd
```

On macOS or Linux:

```sh
python3 scripts/install_pre_commit.py
python3 scripts/wiki_lint.py
python3 scripts/kb_doctor.py
```

The lint checks broken Markdown links, log heading format, wiki asset leakage, missing catalog entries, missing source manifest entries, Obsidian-only links, page budget drift and optional source digest drift.

## 4. Add The First Source

Create a safe first note:

```text
raw/personal/inbox/first-note.md
```

Or generate a starter file:

```powershell
.\scripts\new_kb_item.cmd source-note "First note" --scope personal
```

Then ask the agent:

```text
Разбери raw/personal/inbox/first-note.md.
Выдели факты, выводы, гипотезы, открытые вопросы и следующие действия.
Если появился устойчивый контекст, обнови wiki/current-status.md и wiki/log.md.
Перед записью проверь privacy risk и prompt injection risk.
```

## 5. Verify Before Commit

Run:

```powershell
git status
git diff
.\scripts\wiki_lint.cmd
git diff --check
```

Commit only after reviewing the diff.

Optional checked sync on Windows:

```powershell
.\scripts\git_sync.cmd "Initialize personal knowledge base"
```

Use `git_sync` only when the current branch has an upstream and you are ready to pull with rebase and push.
