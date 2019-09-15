from pydnevnikruapi.dnevnik import DiaryAPI
from datetime import datetime

login = "login"
password = "password"

dn = DiaryAPI(login, password)

print(dn.get_my_school_homework(1000002283077, datetime(2019, 9, 5), datetime(2019, 9, 15)))

