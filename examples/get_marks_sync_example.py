from pydnevnikruapi.dnevnik import dnevnik
import datetime

login = "login"
password = "password"

dn = dnevnik.DiaryAPI(login, password)

context = dn.get_context()
user_id = context["personId"]
school_id = context["schoolIds"][0]

# все оценки юзера
marks = dn.get_person_marks(
    user_id,
    school_id,
    start_time=datetime.datetime.now() - datetime.timedelta(weeks=10),
)

first_mark = marks[0]
mark_subject = dn.get_lesson_info(first_mark["lesson"])
print(mark_subject)
print(
    f"Первая оценка это {first_mark['textValue']} по предмету {mark_subject['subject']['name']} за работу"
    f" {mark_subject['title']}"
)
