<p>
  <img alt="Version" src="https://img.shields.io/badge/version-alpha-blue.svg?cacheSeconds=2592000" />
  <img alt="Python 3.7+" src="https://img.shields.io/badge/Python-3.7+-%23FFD242" />
  <img alt="ШУЕ-ППШ" src="https://img.shields.io/badge/%D0%A8%D0%A3%D0%95-%D0%9F%D0%9F%D0%A8-red" />
  <img alt="The Unlicense" src="https://img.shields.io/badge/license-The%20Unlicense-blue" />
</p>

<h1 align="left">  dnevnik.ru API Wrapper </h1>
<p align="left">Упрощение работы с всероссийским электронным дневником без получения токена.

## Установка

```sh
pip3 install https://github.com/kesha1225/DnevnikRuAPI/archive/master.zip --upgrade

cd DnevnikRuAP
```

## Пример
###### Получение домашнего задания на указанный период.

```python
from pydnevnikruapi import dnevnik
from datetime import datetime

login = "login"
password = "password"

dn = dnevnik.DiaryAPI(login, password)

print(dn.get_my_school_homework(1000002283077, datetime(2019, 9, 5), datetime(2019, 9, 15)))
#  Получение домашнего задания для школы с id 1000002283077 в период с 05-09-2019 по 15-09-2019

print(dn.get_my_edu_groups())
#  Получение групп обучения текущего пользователя
```

## Документация
[api.dnevnik.ru](https://api.dnevnik.ru/partners/swagger/ui/index#/)


 ## TODO:
 1. **Подробная документация на 98 методов.**

 ### Список [контрибьюторов](https://github.com/kesha1225/DnevnikRuAPI/graphs/contributors) данного проекта.

