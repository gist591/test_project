# Lead Distribution CRM

Mini-CRM для автоматического распределения лидов между операторами.

Разработка данного тестового задания полностью по TDD, проект соответствует DDD и чистой архитектуре (Repository, FakeRepository вместо Mock'ов, DI и другое),
покрытие тестами: 1171 88 92%

## Запуск

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Документация: http://localhost:8000/docs

## Тесты

```bash
pytest tests/ -v
```

## Модель данных

- Operator — сотрудник (is_active, max_load)
- Source — источник/бот
- OperatorSource — связь оператор↔источник с weight
- Lead — клиент (идентификация по external_id)
- Contact — обращение (статусы: active, completed, unassigned)

## Алгоритм распределения

1. Фильтрация: активные операторы + не превысили лимит
2. Взвешенный случайный выбор: P(op) = weight / sum(weights)
3. Если нет операторов → статус unassigned

Нагрузка = количество контактов со статусом active

## API

| Метод | Endpoint | Описание |
|-------|----------|----------|
| POST | /operators/ | Создать оператора |
| GET | /operators/ | Список операторов |
| PATCH | /operators/{id} | Обновить оператора |
| POST | /sources/ | Создать источник |
| POST | /sources/{id}/operators | Назначить оператора |
| GET | /sources/{id}/distribution | Настройки распределения |
| POST | /contacts/ | Регистрация обращения |
| GET | /contacts/ | Список обращений |
| GET | /leads/ | Список лидов |
| GET | /leads/{id} | Лид с обращениями |
