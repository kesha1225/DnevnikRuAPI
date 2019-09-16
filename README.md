# dnevnik.ru API Wrapper 
Упрощение работы с всероссийским электронным дневником без получения 
токена.
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-alpha-blue.svg?cacheSeconds=2592000" />
  <img alt="Python 3.7+" src="https://img.shields.io/badge/Python-3.7+-%23FFD242" />
</p>

### Установка

```sh
pip install https://github.com/kesha1225/DnevnikRuAPI/archive/master.zip --upgrade
```

### Пример
Получение домашнего задания на указанный период.

```python
from pydnevnikruapi import DiaryAPI
from datetime import datetime

login = "login"
password = "password"

dn = DiaryAPI(login, password)

print(dn.get_my_school_homework(1000002283077, datetime(2019, 9, 5), datetime(2019, 9, 15)))
```
### Документация
https://api.dnevnik.ru/partners/swagger/ui/index#/
 * TODO: Подробная документация на 98 методов...
