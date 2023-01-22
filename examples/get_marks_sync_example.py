from pydnevnikruapi.dnevnik import dnevnik
import datetime

login = "login"
password = "password"

dn = dnevnik.DiaryAPI(login, password)

context = dn.get_context()
user_id = context["personId"]
school_id = context["schoolIds"][0]
print(user_id, school_id)
print(dn.get_person_marks(user_id, school_id,
                          start_time=datetime.datetime.now() - datetime.timedelta(weeks=10)))
