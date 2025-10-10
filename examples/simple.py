import aiohttp
from pydnevnikruapi import AsyncDiaryAPI
import asyncio
from datetime import datetime


async def get_dn_info():
    dn = AsyncDiaryAPI(
        session=aiohttp.ClientSession(), login="login", password="password"
    )
    await dn.set_token()

    homework = await dn.get_school_homework(
        1000002283077, str(datetime(2019, 9, 5)), str(datetime(2019, 9, 15))
    )
    print(homework)
    edu_groups = await dn.get_edu_groups()
    print(edu_groups)

    await dn.close_session()


if __name__ == "__main__":
    asyncio.run(get_dn_info())
