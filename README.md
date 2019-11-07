<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-alpha-blue.svg?cacheSeconds=2592000" />
  <img alt="Python 3.7+" src="https://img.shields.io/badge/Python-3.7+-%23FFD242" />
  <img alt="code-style" src="https://img.shields.io/badge/code--style-black-%23000000" />
  <img alt="ШУЕ-ППШ" src="https://img.shields.io/badge/%D0%A8%D0%A3%D0%95-%D0%9F%D0%9F%D0%A8-red" />
  <img alt="The Unlicense" src="https://img.shields.io/badge/license-The%20Unlicense-blue" />
</p>

<h1 align="center">  api.dnevnik.ru wrapper </h1>
<p align="center">Упрощение работы с api всероссийского электронного дневника как с токеном, так и без него.

## Установка

```sh
pip install https://github.com/kesha1225/DnevnikRuAPI/archive/master.zip --upgrade
```

## Пример синхронного использования

#### Получение домашнего задания на указанный период без токена.

```python3
from pydnevnikruapi import dnevnik

login = "login"
password = "password"
# Получаем доступ через логин и пароль

dn = dnevnik.DiaryAPI(login=login, password=password)

print(dn.get_school_homework(1000002283077, datetime(2019, 9, 5), datetime(2019, 9, 15)))
#  Получение домашнего задания текущего пользователя для школы с id 1000002283077 в период с 05-09-2019 по 15-09-2019

print(dn.get_edu_groups())
#  Получение групп обучения текущего пользователя
```

## Пример асинхронного использования

#### Получение домашнего задания на указанный период без токена.

```python3
from pydnevnikruapi.async_ import dnevnik
import asyncio
from datetime import datetime


async def get_dn_info():
    await dn.api.get_token()
    #  Получаем токен для использования api

    homework = await dn.get_school_homework(1000002283077, str(datetime(2019, 9, 5)), str(datetime(2019, 9, 15)))
    #  Получение домашнего задания текущего пользователя для школы с id 1000002283077 в период с 05-09-2019 по 15-09-2019
    print(homework)

    edu_groups = await dn.get_edu_groups()
    #  Получение групп обучения текущего пользователя
    print(edu_groups)


async def close_session():
    await dn.api.close_session()
    #  В конце использования закрываем сессию


if __name__ == '__main__':
    login = "login"
    password = "password"
    dn = dnevnik.DiaryAPI(login=login, password=password)
    # Получаем доступ через логин и пароль

    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_dn_info())
    loop.run_until_complete(close_session())
    # Запускаем все наши функции в event loop
```

## Документация

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
    dn = dnevnik.DiaryAPI(login=login, password=password)
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
    dn = dnevnik.DiaryAPI(token=token)
    # Получаем доступ через токен

    loop = asyncio.get_event_loop()
    loop.run_until_complete(close_session())
    # Запускаем все наши функции в event loop
```

## Методы dnevnik.ru:

### Authorities

- get_organizations - Список идентификаторов организаций текущего пользователя
```python
dn.get_organizations()
```

- get_organization_info - Данные указанной организации пользователя
```python
dn.get_organization_info()
```

### AverageMarks

- get_person_average_marks - Оценки персоны за отчетный период
```python
dn.get_person_average_marks(person_id=1000002385955, period=1000002385971)
```
|Параметр|Описание|
|-|-|
|person_id|ID выбранной персоны|
|period|Период для получения оценок в unixtime|

- get_person_average_marks_by_subject - Оценка персоны по предмету за отчетный период
```python
dn.get_person_average_marks_by_subjects(person_id=1000002385955, period=1000002385971, subject_id=683725334)
```
|Параметр|Описание|
|-|-|
|person_id|ID выбранной персоны|
|period|Период для получения оценок в unixtime|
|subject_id|ID выбранного предмета|

- get_group_average_marks_by_date - Оценки учебной группы по предмету за отчетный период до определенной даты
```python
import datetime

dn.get_group_average_marks_by_date(group_id=14455222, period=1000002385971, date=datetime.datetime(2019, 11, 8))
```
|Параметр|Описание|
|-|-|
|group_id|ID выбранной учебной группы|
|period|Период для получения оценок в unixtime|
|date|Конечная дата|

- get_group_average_marks_by_time - Оценки учебной группы за период
```python
import datetime

dn.get_group_average_marks_by_time(group_id=14455222, start_time=datetime.datetime(2019, 11, 5),
                                   end_time=datetime.datetime(2019, 11, 8))
```
|Параметр|Описание|
|-|-|
|group_id|ID выбранной учебной группы|
|start_time|Начальное время для получения оценок в unixtime|
|end_time|Конечное время для получения оценок в unixtime|

### Children

- get_user_children - Получение списка детей по идентификатору родительского пользователя
```python
dn.get_user_children(user_id=1000001509233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

- get_person_children - Получение списка детей по идентификатору родительской персоны
```python
dn.get_person_children(person_id=1000002385971)
```
|Параметр|Описание|
|-|-|
|person_id|ID выбранной персоны|

### Classmates

- get_classmates - Список id пользователей одноклассников текущего пользователя,
 если он является учеником, либо список активных участников образовательных групп пользователя во всех остальных случаях
```python
dn.get_classmates()
```

### Context

- get_context - Получение контекстной информации по пользователю
```python
dn.get_context()
```

- get_user_context - Получение контекстной информации по пользователю
```python
dn.get_user_context(user_id=1000001509233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

### CriteriaJournalMarks

- get_final_group_marks_by_subject - Метод, позволяющий получить итоговые оценки всего класса по указанному предмету
```python
dn.get_final_group_marks_by_subject(group_id=10033, subject_id=45666212)
```
|Параметр|Описание|
|-|-|
|group_id|ID выбранной группы|
|subject_id|ID выбранного предмета|

- get_final_group_marks - Метод, позволяющий получить итоговые оценки всего класса (каждого ученика) по всем предметам
```python
dn.get_final_group_marks(group_id=10033)
```
|Параметр|Описание|
|-|-|
|group_id|ID выбранной группы|

### EducationMemberships

- get_user_memberships - Список участий в школах для произвольного пользователя
```python
dn.get_user_memberships(user_id=1000001509233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

- get_user_education - Список участий в школах для произвольной персоны
```python
dn.get_user_education(person_id=1000001433233)
```
|Параметр|Описание|
|-|-|
|person_id|ID выбранной персоны|

- get_schools - Список идентификаторов школ текущего пользователя
```python
dn.get_schools()
```

- get_user_schools - Список идентификаторов школ произвольного пользователя
```python
dn.get_user_schools(user_id=1000005000233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

- get_edu_groups - Список идентификаторов классов текущего пользователя
```python
dn.get_edu_groups(user_id=1000005000233)
```

- get_user_edu_groups - Список идентификаторов классов произвольного пользователя
```python
dn.get_user_schools(user_id=1000005000233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

- get_memberships - Список участий в школах для текущего пользователя
```python
dn.get_memberships()
```

### EduGroups






## Документация на сайте

[api.dnevnik.ru](https://api.dnevnik.ru/partners/swagger/ui/index#/)


