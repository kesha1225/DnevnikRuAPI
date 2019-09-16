# dnevnik.ru API Wrapper 
Упрощение работы с всероссийским электронным дневником без получения 
токена.
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-alpha-blue.svg?cacheSeconds=2592000" />
  <img alt="Python 3.7+" src="https://img.shields.io/badge/Python-3.7+-%23FFD242" />
  <img alt="ШУЕ-ППШ" src="https://img.shields.io/badge/%D0%A8%D0%A3%D0%95-%D0%9F%D0%9F%D0%A8-red" />
  <img alt="The Unlicense" src="https://img.shields.io/badge/license-The%20Unlicense-blue" />
</p>

### Установка

```sh
pip install https://github.com/kesha1225/DnevnikRuAPI/archive/master.zip --upgrade
```

### Пример
Получение домашнего задания на указанный период.

```python
from pydnevnikruapi import dnevnik
from datetime import datetime

login = "login"
password = "password"

dn = dnevnik.DiaryAPI(login, password)

print(dn.get_my_school_homework(1000002283077, datetime(2019, 9, 5), datetime(2019, 9, 15)))
#  Домашнее задание для школы с id 1000002283077 с 2019-09-05 по 2019-09-15

print(dn.get_my_edu_groups())
#  Образовательные группы текущего пользователя
```
### Документация
https://api.dnevnik.ru/partners/swagger/ui/index#/
 * TODO: Подробная документация на 98 методов...
