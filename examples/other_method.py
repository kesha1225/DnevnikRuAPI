from pydnevnikruapi.dnevnik import dnevnik


dn = dnevnik.DiaryAPI(login="login", password="password")

# Допустим тут метод которого нет в библиотеке, но он есть в доке свагера
user_info = dn.get(f"users/me")
print(user_info)
# То же самое с пост методами и тд (это работать не будет, просто пример)
lesson_log = dn.post(
    f"lessons/123/log-entries",
    data={"lessonLogEntry": "data"},
)
