# JEV Agent

Типизированные кейсы TypeSafe: входные данные, вопросы и ответы — Pydantic-объекты.

Установите зависимости через `uv sync` и укажите `JEV_API_KEY` в `.env`
(образец — `.env.example`).

| Кейс | State в API | Задача | Запуск |
| --- | --- | --- | --- |
| `ticket` | Строка | Отдел, недовольство, срочность | `uv run python -m src.main ticket` |
| `refund` | Вложенный объект | Запрос возврата, повторное списание, соответствие политике | `uv run python -m src.main refund` |
| `conversation` | Массив объектов | Запрос оператора и повторное обращение | `uv run python -m src.main conversation` |

Без аргумента запускается `ticket`.

`state` — материал для оценки: сообщение, диалог, заказ, политика или связанные
данные приложения. API принимает строку, объект или массив. В коде строка
представлена `TicketState(RootModel[str])`, массив —
`ConversationState(RootModel[list[Message]])`, объект — `RefundState(BaseModel)`.
Вложенные объекты могут содержать текст, числа, списки и другие поля контекста.

`questions` — именованный набор вопросов об этом материале. Каждый вопрос имеет
тип (`Choice`, `Score`, `Noul`), инструкции и, при необходимости, критерии.
Имя поля связывает вопрос с ответом; сам вопрос нужно полностью сформулировать
в `instructions`. Все вопросы одного запроса используют один state и оцениваются
независимо. Для зависимого вопроса нужен новый запрос с обновлённым контекстом.

`Choice` выбирает вариант, `Score` оценивает по упорядоченным уровням, `Noul`
возвращает вероятность истинности от 0 до 1. `instructions` и описания критериев
могут быть структурированными. В кейсе `refund` поле `PolicyQuestion.instructions`
описано отдельной Pydantic-схемой `PolicyInstructions`.

Каждый модуль в `src/cases/` содержит свои state, вопросы, ответы и класс кейса.
Общие модели находятся в `src/schemas.py`, вызов SDK — в `src/client.py`.
`RootModel` сериализуется непосредственно в строку или массив без обёртки `root`.
Преобразование моделей в формат API выполняется только внутри адаптера.
SDK проверяет ответ через `response_model`; ручного разбора JSON нет.

```python
from src.cases.refund import RefundCase

case = RefundCase()
case.state.order.id
case.questions.policy_supports_refund.instructions.focus
response = await case.run(client)
response.answers.policy_supports_refund.noul
response.usage.input_tokens
```

Схемы state можно передать при создании кейса вместо демонстрационных данных.

Документация TypeSafe: [State](https://docs.typesafe.ai/concepts/state),
[Questions](https://docs.typesafe.ai/primitives),
[структурированные инструкции и критерии](https://docs.typesafe.ai/primitives/advanced),
[собственная схема ответа](https://docs.typesafe.ai/sdk/python/usage#custom-response-types).
