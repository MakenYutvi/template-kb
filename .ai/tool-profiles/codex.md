# Профиль Codex

Codex используется как основной агент для работы с этим репозиторием.

## Как начинать сессию

Попросите Codex:

```text
Прочитай AGENTS.md, .ai/contract.md, .ai/privacy.md и wiki/workflows/context-budget.md.
Для общего контекста используй wiki/index.md и нужную область wiki/current-status.md.
Скажи, какой контекст ты восстановил, и предложи следующий маленький шаг.
```

## Типовые задачи

- разложить новую заметку из `raw/personal/inbox/`;
- составить план проекта;
- обновить `wiki/current-status.md`;
- сохранить substantial generated output в `wiki/outputs/`;
- зафиксировать health/lint report в `wiki/health/`;
- сделать writeback после сессии;
- проверить `git diff` перед commit;
- подготовить список следующих действий.

## Правило качества

Codex должен отделять факты, выводы и гипотезы, когда работает с важными
решениями.
