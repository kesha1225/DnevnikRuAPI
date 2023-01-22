from pydnevnikruapi.dnevnik import dnevnik


dn = dnevnik.DiaryAPI(login="login", password="password")

# допустим тут метод которого нет в библиотеке но он есть в доке свагера
context = dn.get(f"users/me/context")
print(context)
# то же самое с пост методами итд (это работать не будет просто прмиер)
lesson_log = dn.post(
    f"lessons/123/log-entries",
    data={"lessonLogEntry": "data"},
)
