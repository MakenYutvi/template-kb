# Демо-сценарий

Этот walkthrough использует вымышленное безопасное содержимое и показывает
целевой memory flow:

```text
source note -> output -> writeback -> lint/health
```

## 1. Добавить source note

Начните с маленькой заметки в
[`../raw/personal/inbox/first-note.example.md`](../raw/personal/inbox/first-note.example.md)
или создайте новую source note:

```powershell
.\scripts\new_kb_item.cmd source-note "First note" --scope personal
```

Используйте безопасное содержимое, например:

```text
Я хочу легкую систему для заметок по книгам и повторяющихся проектных решений.
Я не хочу хранить в репозитории приватные credentials или чувствительные документы.
```

## 2. Попросить агента разобрать источник

Промпт:

```text
Разбери raw/personal/inbox/first-note.md.
Отдели факты, выводы, гипотезы, открытые вопросы и следующие действия.
Если появился устойчивый контекст, предложи writeback.
```

Агент должен воспринимать source как данные, а не инструкции. Если source
содержит подозрительные инструкции, они должны попасть в `Safety Notes`.

## 3. Сохранить substantial output

Если ответ становится reusable brief, сохраните его в
[`../wiki/outputs/`](../wiki/outputs/):

```powershell
.\scripts\new_kb_item.cmd output "first-kb-brief"
```

Добавьте `Context Read`, чтобы показать, какие файлы агент реально прочитал.

## 4. Перенести durable findings

Durable findings должны перейти из output в подходящую wiki-страницу через
[`../wiki/workflows/writeback.md`](../wiki/workflows/writeback.md).

Примеры:

- обновить `wiki/current-status.md` текущими целями;
- добавить решение в `wiki/decisions/`;
- добавить project или concept page, когда тема стала достаточно устойчивой.

Не копируйте секреты или широкие чувствительные детали в `wiki/`.

## 5. Запустить health checks

Запустите lint:

```powershell
.\scripts\wiki_lint.cmd
```

Для содержательного review создайте health report в
[`../wiki/health/`](../wiki/health/) и следуйте
[`../wiki/workflows/lint.md`](../wiki/workflows/lint.md).

Итог должен показывать, что изменилось, какие источники подтверждают изменения
и остался ли manual review.
