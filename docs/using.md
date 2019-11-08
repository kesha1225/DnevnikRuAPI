# Вариации использования

### Начало работы

Импортируем библиотеку и получаем доступ к api с помощью токена или логина и пароля

**Синхронно** без токена
```python
from pydnevnikruapi import dnevnik
from datetime import datetime

login = "login"
password = "password"

dn = dnevnik.DiaryAPI(login=login, password=password)
```

**Синхронно** с токеном
```python
from pydnevnikruapi import dnevnik
from datetime import datetime

token = "fuLNdxicTuDpfEC8Xc4eu57RTU67vAjJ"

dn = dnevnik.DiaryAPI(token=token)
```

**Асинхронно** без токена
```python3
from pydnevnikruapi.async_ import dnevnik
import asyncio


async def get_token():
    await dn.api.get_token()
    # Получаем токен


async def close_session():
    await dn.api.close_session()
    #  В конце использования закрываем сессию


if __name__ == '__main__':
    login = "login"
    password = "password"
    dn = dnevnik.AsyncDiaryAPI(login=login, password=password)
    # Получаем доступ через логин и пароль

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_token())
    loop.run_until_complete(close_session())
    # Запускаем все наши функции в event loop
```

**Асинхронно** с токеном, *функция dn.api.get_token() нам не нужна*
```python3
from pydnevnikruapi.async_ import dnevnik
import asyncio
from datetime import datetime


async def close_session():
    await dn.api.close_session()
    #  В конце использования закрываем сессию


if __name__ == '__main__':
    token = "uqLp5xicTurpTEC8Xc4eup7R6U77bhl0"
    dn = dnevnik.AsyncDiaryAPI(token=token)
    # Получаем доступ через токен

    loop = asyncio.get_event_loop()
    loop.run_until_complete(close_session())
    # Запускаем все наши функции в event loop
```