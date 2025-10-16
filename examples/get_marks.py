import asyncio

import aiohttp

from pydnevnikruapi import AsyncDiaryAPI
import datetime


async def main():
    dn = AsyncDiaryAPI(
        session=aiohttp.ClientSession(), login="login", password="password"
    )
    await dn.set_token()
    context = await dn.get_context()
    user_id = context["personId"]
    school_id = context["schoolIds"][0]
    print(user_id, school_id)
    print(
        await dn.get_person_marks(
            user_id,
            school_id,
            start_time=str(datetime.datetime.now() - datetime.timedelta(weeks=10)),
        )
    )
    await dn.close_session()


if __name__ == "__main__":
    asyncio.run(main())
