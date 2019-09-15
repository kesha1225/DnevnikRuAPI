# dnevnik.ru API Wrapper 
Упрощение работы с всероссийским электронным дневником без получения 
токена.

> Alpha
### Установка
```bash
pip install https://github.com/kesha1225/DnevnikRuAPI/archive/master.zip
```
### Простой пример получения домашней работы на указанный период
```python
from pydnevnikruapi.dnevnik import DiaryAPI
from datetime import datetime

login = "login"
password = "password"

dn = DiaryAPI(login, password)

print(dn.get_my_school_homework(1000002283077, datetime(2019, 9, 5), datetime(2019, 9, 15)))
```