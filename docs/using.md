# Вариации использования

### Начало работы

Импортируем библиотеку и получаем доступ к api с помощью токена или логина и пароля

**Синхронно** без токена
```python
from pydnevnikruapi.dnevnik import dnevnik

login = "login"
password = "password"

dn = dnevnik.DiaryAPI(login=login, password=password)
```

**Синхронно** с токеном
```python
from pydnevnikruapi.dnevnik import dnevnik

token = "fuLNdxicTuDpfEC8Xc4eu57RTU67vAjJ"

dn = dnevnik.DiaryAPI(token=token)
```

**Асинхронно** без токена
```python3
from pydnevnikruapi.aiodnevnik import dnevnik
from pydnevnikruapi.aiodnevnik.utils import TaskManager
import asyncio

async def close_session():
    await dn.api.close_session()
    #  В конце использования закрываем сессию


if __name__ == "__main__":
    login = "login"
    password = "password"
    dn = dnevnik.AsyncDiaryAPI(login=login, password=password)
    # Получаем доступ через логин и пароль

    loop = asyncio.get_event_loop()
    # Добавляем все наши функции в event loop через Task Manager

    task_manager = TaskManager(loop)
    task_manager.run(on_shutdown=close_session)
    # Закрываем сессию по завершению работы

```

**Асинхронно** с токеном
```python3
from pydnevnikruapi.aiodnevnik import dnevnik
from pydnevnikruapi.aiodnevnik.utils import TaskManager
import asyncio


async def do_something():
    pass
    #  Какая-либо функция


async def close_session():
    await dn.close_session()
    #  В конце использования закрываем сессию


if __name__ == "__main__":
    token = "uqLp5xicTurpTEC8Xc4eup7R6U77bhl0"
    dn = dnevnik.AsyncDiaryAPI(token=token)
    # Получаем доступ через токен

    loop = asyncio.get_event_loop()
    # Добавляем все наши функции в event loop через Task Manager

    task_manager = TaskManager(loop)
    task_manager.add_task(do_something)
    task_manager.run(on_shutdown=close_session)
    # Закрываем сессию по завершению работы

```