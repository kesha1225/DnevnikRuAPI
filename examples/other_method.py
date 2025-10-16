import asyncio
import aiohttp
from pydnevnikruapi import AsyncDiaryAPI


async def main():
    dn = AsyncDiaryAPI(
        session=aiohttp.ClientSession(), login="login", password="password"
    )
    await dn.set_token()

    # Допустим тут метод которого нет в библиотеке, но он есть в доке свагера
    user_info = await dn.get(f"users/me")
    print(user_info)
    # То же самое с пост методами и тд (это работать не будет, просто пример)
    lesson_log = await dn.post(
        f"lessons/123/log-entries",
        data={"lessonLogEntry": "data"},
    )
    print(lesson_log)

    await dn.close_session()


asyncio.run(main())
