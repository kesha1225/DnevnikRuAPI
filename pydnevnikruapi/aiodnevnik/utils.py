import asyncio
import typing
from .exceptions import AsyncDiaryError


class TaskManager:
    def __init__(self, loop: asyncio.AbstractEventLoop):
        self.tasks: typing.List[typing.Callable] = []
        self.loop = loop

    def add_task(self, task: typing.Callable):
        if asyncio.iscoroutinefunction(task):
            self.tasks.append(task)
        else:
            raise AsyncDiaryError("Таск может быть только корутиной")

    async def __run(self):
        if not self.tasks:
            raise AsyncDiaryError("Таск менеджер получил 0 заданий")

        [await self.loop.create_task(task()) for task in self.tasks]

    def run(self, on_shutdown: typing.Callable = None):
        try:
            self.loop.run_until_complete(self.__run())
        finally:
            if on_shutdown is not None:
                self.loop.run_until_complete(on_shutdown())
