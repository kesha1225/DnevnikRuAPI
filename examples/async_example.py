from pydnevnikruapi.async_ import dnevnik
import asyncio
from datetime import datetime
from pydnevnikruapi.async_.utils import TaskManager


async def get_dn_info():
    await dn.api.get_token()
    homework = await dn.get_school_homework(
        1000002283077, str(datetime(2019, 9, 5)), str(datetime(2019, 9, 15))
    )
    print(homework)
    edu_groups = await dn.get_edu_groups()
    print(edu_groups)


async def close_session():
    await dn.api.close_session()


if __name__ == "__main__":
    dn = dnevnik.AsyncDiaryAPI("login", "password")

    loop = asyncio.get_event_loop()
    task_manager = TaskManager(loop)
    task_manager.add_task(get_dn_info)
    task_manager.run(on_shutdown=close_session)
