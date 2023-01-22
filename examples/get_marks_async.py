import asyncio

from pydnevnikruapi.aiodnevnik import dnevnik
import datetime

login = "login"
password = "password"


async def main(dn):
    context = await dn.get_context()
    user_id = context["personId"]
    school_id = context["schoolIds"][0]
    print(user_id, school_id)
    print(
        await dn.get_person_marks(
            user_id,
            school_id,
            start_time=datetime.datetime.now() - datetime.timedelta(weeks=10),
        )
    )


if __name__ == "__main__":
    dn_ = dnevnik.AsyncDiaryAPI(login, password)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(dn_))
