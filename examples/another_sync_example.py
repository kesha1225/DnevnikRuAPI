from pydnevnikruapi.dnevnik import dnevnik

login = "login"
password = "password"

with dnevnik.DiaryAPI(login=login, password=password) as dn:
    print(dn.get_classmates())

    print(dn.get_context())
