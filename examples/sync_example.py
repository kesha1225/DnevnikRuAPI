from pydnevnikruapi.sync import dnevnik
from datetime import datetime

login = "login"
password = "password"

dn = dnevnik.DiaryAPI(login, password)

print(
    dn.get_school_homework(1000002283077, datetime(2019, 9, 5), datetime(2019, 9, 15))
)

print(dn.get_edu_groups())
