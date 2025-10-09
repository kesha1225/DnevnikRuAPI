from pydnevnikruapi.dnevnik import dnevnik

login = "login"
password = "password"

with dnevnik.DiaryAPI(login=login, password=password) as dn:
    feed = dn.get_feed()
    print(feed)
    info = dn.get_info()
    print(info)
