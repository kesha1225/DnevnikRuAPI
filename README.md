<p align="center">
  <img alt="Version" src="https://img.shields.io/badge/version-beta-blue" />
  <img alt="Python 3.13+" src="https://img.shields.io/badge/Python-3.13+-%23FFD242" />
  <img alt="code-style" src="https://img.shields.io/badge/code--style-black-%23000000" />
  <img alt="ШУЕ-ППШ" src="https://img.shields.io/badge/%D0%A8%D0%A3%D0%95-%D0%9F%D0%9F%D0%A8-red" />
  <img alt="The Unlicense" src="https://img.shields.io/badge/license-The%20Unlicense-blue" />
</p>

<h1 align="center">api.dnevnik.ru wrapper</h1>
<p align="center">Упрощение работы с api всероссийского электронного дневника как с токеном, так и без него.</p>

## ⚙️ Установка

```sh
pip install pydnevnikruapi
```
или
```sh
pip install https://github.com/kesha1225/DnevnikRuAPI/archive/master.zip --upgrade
```

## ℹ️ Документация

По методам API - https://api.dnevnik.ru/partners/swagger/ui/index

> [!CAUTION]
> Некоторые методы могут быть недоступны, ниже представлен список поддерживаемых эндпоинтов.

> [!NOTE]
> Библиотека поддерживает только асинхронное использование (async/await).

## Пример использования

#### Получение домашнего задания на указанный период

```python3
import aiohttp
from pydnevnikruapi import AsyncDiaryAPI
import asyncio
from datetime import datetime


async def get_dn_info():
    async with aiohttp.ClientSession() as session:
        dn = AsyncDiaryAPI(session=session, login="login", password="password")
        await dn.set_token()

        homework = await dn.get_school_homework(
            1000002283077, 
            datetime(2019, 9, 5).isoformat(), 
            datetime(2019, 9, 15).isoformat()
        )
        print(homework)
        
        edu_groups = await dn.get_edu_groups()
        print(edu_groups)


if __name__ == "__main__":
    asyncio.run(get_dn_info())
```

## Использование с токеном

```python3
import aiohttp
from pydnevnikruapi import AsyncDiaryAPI
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        # Используем существующий токен
        dn = AsyncDiaryAPI(session=session, token="your_token_here")
        
        user_info = await dn.get_info()
        print(user_info)


if __name__ == "__main__":
    asyncio.run(main())
```

## Пример использования неописанного метода

Если нужного метода нет в библиотеке, но он есть в документации API:

```python3
import asyncio
import aiohttp
from pydnevnikruapi import AsyncDiaryAPI


async def main():
    async with aiohttp.ClientSession() as session:
        dn = AsyncDiaryAPI(session=session, login="login", password="password")
        await dn.set_token()

        # Прямое использование API методов
        user_info = await dn.get("users/me")
        print(user_info)
        
        # POST запрос (пример)
        lesson_log = await dn.post(
            "lessons/123/log-entries",
            data={"lessonLogEntry": "data"},
        )
        print(lesson_log)


if __name__ == "__main__":
    asyncio.run(main())
```

## 🗒️ Список поддерживаемых API эндпоинтов, а также их соотношение с функциями


- [x] /v2.0/users/me/organizations -  **get_organizations()** - Список идентификаторов организаций текущего пользователя

- [x] /v2.0/users/me/organizations/{organizationId} -  **get_organization_info(organization_id: int)** - Данные указанной организации пользователя

- [x] /v2.0/authorizations -  **get_token(login, password)** - Обменять код доступа на токен

- [x] /v2.0/persons/{person}/reporting-periods/{period}/avg-mark - **get_person_average_marks(person: int, period: int)** - Оценки персоны за отчетный период

- [x] /v2.0/edu-groups/{group}/reporting-periods/{period}/avg-marks/{date} - **get_group_average_marks_by_date( group_id: int, period: int, date: datetime.datetime)** - Оценки учебной группы по предмету за отчетный период до определенной даты

- [x] /v2.0/edu-groups/{group}/avg-marks/{from}/{to} - **get_group_average_marks_by_time(group_id: int, start_time: datetime.datetime, end_time: datetime.datetime)** - Оценки учебной группы за период

- [x] /v2.0/user/{userID}/children - **get_user_children(user_id: int)** - Получение списка детей по идентификатору родительского пользователя

- [x] /v2.0/person/{personID}/children - **get_person_children(person_id: int)** - Получение списка детей по идентификатору родительской персоны

- [x] /v2.0/users/me/classmates - **get_classmates()** - Список id пользователей одноклассников текущего пользователя, если он является учеником, либо список активных участников образовательных групп пользователя во всех остальных случаях

- [ ] /v2.0/users/me/context - **get_context()** - Получение контекстной информации по пользователю

- [ ] /v2.0/users/{userId}/context - **get_user_context(user_id: int)** - Получение контекстной информации по пользователю

- [x] /v2.0/edu-group/{group}/subject/{subject}/period/{period}/criteria-marks-sections - **func** - Метод получения списка секций СОр + СОч для класса по предмету в выбранном периоде c соответствующей информацией

- [x] /v2.0/edu-group/{group}/person/{person}/subject/{subject}/period/{period}/criteria-marks - **func** - Метод получения суммативных оценок (СОр, СОч) ученика класса по предмету за период, с привязкой к конкретной теме/суммативной оценки четверти

- [x] /v2.0/edu-group/{group}/period/{period}/criteria-marks - **func** - Метод получения списка оценок (СОр, СОч) класса сгруппированные по ученикам и предметам за период (т.е. оценки каждого ученика класса, разбитые по предметам)

- [x] /v2.0/edu-group/{group}/subject/{subject}/period/{period}/criteria-marks - **func** - Метод получения всех оценок (СОр и СОч) класса (группировка по ученикам) за период по выбранному предмету

- [x] /v2.0/edu-group/{group}/criteria-marks-totals - **get_final_group_marks(group_id: int)** - Метод, позволяющий получить итоговые оценки всего класса (каждого ученика) по всем предметам

- [x] /v2.0/edu-group/{group}/subject/{subject}/criteria-marks-totals - **get_final_group_marks_by_subject(group_id: int, subject_id: int)** - Метод, позволяющий получить итоговые оценки всего класса по указанному предмету

- [x] /v2.0/edu-group/{group}/criteriajournalsection/{section}/criteria-marks - **func** - Метод полученипя списка суммативных оценок класса за конкретную тему (СОр или СОч по section_id параметру, который является связывающим звеном для оценок одной темы)

- [x] /v2.0/edu-group/{group}/criteriajournalsection/{section}/criteria-marks-totals - **func** - Метод полученипя списка итоговых суммативных оценок класса за конкретную тему (СОр или СОч по section_id параметру, который является связывающим звеном для сумативной оценки за четверть)

- [x] /v2.0/users/{user}/school-memberships - **get_user_memberships(user_id: int)** - Список участий в школах для произвольного пользователя

- [x] /v2.0/users/{user}/education - **get_user_education(user_id: int)** - Список участий в школах для произвольного пользователя

- [x] /v2.0/persons/{person}/school-memberships - **get_person_memberships(person_id: int)** - Список участий в школах для произвольной персоны

- [x] /v2.0/users/me/schools - **get_schools()** - Список идентификаторов школ текущего пользователя

- [x] /v2.0/users/{user}/schools - **get_user_schools(user_id: int)** - Список идентификаторов школ произвольного пользователя

- [x] /v2.0/users/me/edu-groups - **get_edu_groups()** - Список идентификаторов классов текущего пользователя

- [x] /v2.0/users/{user}/edu-groups - **get_user_edu_groups(user_id: int)** - Список идентификаторов классов текущего пользователя

- [x] /v2.0/users/me/school-memberships - **get_memberships()** - Список участий в школах для текущего пользователя

- [x] /v2.0/edu-groups/{eduGroup} - **get_group_info(edu_group_id: int)** - Класс или учебная группа

- [x] /v2.0/edu-groups - **get_groups_info(edu_groups_list: list)** - Список учебных групп

- [x] /v2.0/schools/{school}/edu-groups - **get_school_groups(school_id: int)** - Список классов в школе

- [x] /v2.0/persons/{person}/edu-groups - **get_person_groups(person_id: int)** - Учебные группы персоны

- [x] /v2.0/persons/{person}/edu-groups/all - **get_person_groups_all(person_id: int)** - 123

- [x] /v2.0/persons/{person}/schools/{school}/edu-groups - **get_person_school_groups(person_id: int, school_id: int)** - Учебные группы персоны в школе

- [x] /v2.0/edu-groups/{group}/persons - **get_groups_pupils(edu_group_id: int)** - Список учеников учебной группы

- [x] /v2.0/edu-groups/students - **get_students_groups_list()** - Список групп с учениками

- [x] /v2.0/edu-groups/{groupId}/parallel - **get_groups_parallel(group_id: int)** - Список параллельных групп(включая группу указанную в параметрах)

- [x] /authorizations/esia/v2.0/users/linked - **func** - 123

- [x] /authorizations/esia/v2.0 - **func** - 123

- [x] /v2.0/files/async/upload - **func** - Метод загрузки файла. Файл будет загружен в первую папку привязанной к приложению сети. При загрузке файла обязательно надо передать заголовки Content-Type: multipart/form-data с соотвествующим boundary и верный Content-Length. 

- [x] /v2.0/folder/{folderId}/files/async/upload - **func** - Метод для загрузки файла в папку. При загрузке файла обязательно надо передать заголовки Content-Type: multipart/form-data с соотвествующим boundary и верный Content-Length.

- [x] /v2.0/files/async/upload/base64 - **func** - Метод загрузки файла в формате строки base64. При загрузке файла обязательно надо передать заголовки Content-Type: application/json, а бинарные данные файла передать в теле запроса. Файл будет загружен в первую папку привязанной к приложению сети. 

- [x] /v2.0/files/async/upload/{taskId} - **func** - Метод получения загруженного файла.

- [x] /v2.0/files/{fileId}/repost - **func** - Репост файла

- [x] /v2.0/folder/{folderId}/files - **func** - Получение файлов в папке

- [x] /v2.0/apps/current/files - **func** - Получение файлов приложения

- [x] /v2.0/files/{fileId}/like - **func** - Увеличения количества лайков/голосов на единицу

- [x] /v2.0/edu-groups/{group}/final-marks - **get_group_marks(group_id: int)** - Оценки в учебной группе

- [x] /v2.0/persons/{person}/edu-groups/{group}/final-marks - **get_person_group_marks(person_id: int, group_id: int)** - Оценки персоны в учебной группе

- [x] /v2.0/persons/{person}/edu-groups/{group}/allfinalmarks - **get_person_group_marks_final(person_id: int, group_id: int)** - Итоговые оценки персоны в учебной группе

- [x] /v2.0/edu-groups/{group}/subjects/{subject}/final-marks - **get_group_subject_final_marks(group_id: int, subject_id: int)** - Оценки по предмету в учебной группе

- [ ] /v2.0/users/me/friends - **get_friends()** - Список id пользователей друзей текущего пользователя

- [ ] /v2.0/users/{user}/friends - **get_user_friends(user_id: int)** - Список id пользователей друзей конкретного пользователя по его id

- [x] /v2.0/users/me/school/{school}/homeworks - **def get_school_homework(school_id: int, start_time: datetime.datetime, end_time: datetime.datetime):** - Получить домашние задания пользователя за период времени

- [x] /v2.0/users/me/school/homeworks - **get_homework_by_id(homework_id: int)** - Получить домашние задания по идентификаторам

- [x] /v2.0/persons/{person}/school/{school}/homeworks - **get_person_homework(school_id: int,person_id: int, start_time: datetime.datetime, end_time: datetime.datetime):** - Получить домашние задания обучающегося за период времени

- [x] /v2.0/works/{workId}/test - **func** - Прикрепить тест к дз

- [x] /v2.0/lessons/{lesson}/log-entries - **delete_lesson_log(lesson_id: int, person_id: int)** - Список отметок о посещаемости на уроке

- [x] /v2.0/lesson-log-entries - **get_lesson_logs(lessons_ids: list)** - Список отметок о посещаемости на нескольких уроках

- [x] /v2.0/lesson-log-entries/lesson/{lesson}/person/{person} - **get_person_lesson_log(person_id: int, lesson_id: int)** - Отметка о посещаемости ученика на уроке

- [x] /v2.0/lesson-log-entries/group/{eduGroup} - **get_group_lesson_log(group_id: int, subject_id: int, start_time: datetime.datetime, end_time: datetime.datetime)** - Список отметок о посещаемости на уроках по заданному предмету в классе за интервал времени

- [x] /v2.0/lesson-log-entries/person/{personID}/subject/{subjectID} - **func** - Список отметок о посещаемости обучающегося по предмету за интервал времени

- [x] /v2.0/lesson-log-entries/person={personID}&subject={subjectID}&from={from}&to={to} - **get_person_subject_lesson_log(person_id: int,subject_id: int,start_time: datetime.datetime,end_time: datetime.datetime)** - Список отметок о посещаемости обучающегося по предмету за интервал времени

- [x] /v2.0/persons/{person}/lesson-log-entries - **get_person_lesson_logs(person_id: int, start_time: datetime.datetime, end_time: datetime.datetime)** - Список отметок о посещаемости обучающегося за интервал времени

- [x] /v2.0/lesson-log-entries/statuses - **get_lesson_log_statuses()** - Получить список возможных отметок о посещаемости. Пример ответа - ["Attend","Absent","Ill","Late","Pass"].

- [x] /v2.0/lessons/{lesson} - **get_lesson_info(lesson_id: int)** - Получить урок с заданным id

- [x] /v2.0/lessons/many - **get_many_lessons_info(lessons_list: list)** - Получение списка уроков по списку id

- [x] /v2.0/edu-groups/{group}/lessons/{from}/{to} - **get_group_lessons_info(group_id: int, start_time: datetime.datetime, end_time: datetime.datetime)** - Уроки группы за период

- [x] /v2.0/edu-groups/{group}/subjects/{subject}/lessons/{from}/{to} - **get_group_lessons_info(group_id: int, start_time: datetime.datetime, end_time: datetime.datetime)** - Уроки группы по предмету за период

- [x] /v2.0/works/{workID}/marks/histogram - **get_marks_histogram(work_id: int)** - Получение деперсонализированной гистограмы оценок всего класса по идентификатору работы

- [x] /v2.0/periods/{periodID}/subjects/{subjectID}/groups/{groupID}/marks/histogram - **get_subject_marks_histogram(group_id: int, period_id: int, subject_id: int)** - Получение деперсонализированной гистограмы оценок всего класса за отчетный период

- [x] /v2.0/marks/{mark} - **get_mark_by_id(mark_id: int)** - Оценка

- [x] /v2.0/works/{work}/marks - **get_marks_by_work(work_id: int)** - Список оценок за работу на уроке

- [x] /v2.0/lessons/{lesson}/marks - **get_marks_by_lesson(lesson_id: int)** - Оценки на уроке

- [x] /v2.0/lessons/marks - **get_marks_by_lessons(lessons_ids: list)** - Список оценок за несколько уроков

- [x] /v2.0/lessons/many/marks - **func** - Список оценок за несколько уроков

- [x] /v2.0/edu-groups/{group}/marks/{from}/{to} - **get_group_marks_period(group_id: int,start_time: datetime.datetime, end_time: datetime.datetime)** - Оценки учебной группы за период

- [x] /v2.0/edu-groups/{group}/subjects/{subject}/marks/{from}/{to} - **get_group_subject_marks(group_id: int, subject_id: int, start_time: datetime.datetime, end_time: datetime.datetime)** - Оценки учебной группы по предмету за период

- [x] /v2.0/persons/{person}/schools/{school}/marks/{from}/{to} - **get_person_marks(person_id: int, school_id: int, start_time: datetime.datetime, end_time: datetime.datetime)** - Оценки персоны в школе за период

- [x] /v2.0/persons/{person}/edu-groups/{group}/marks/{from}/{to} - **func** - Оценки персоны в учебной группе за период

- [x] /v2.0/persons/{person}/lessons/{lesson}/marks - **get_person_lessons_marks(person_id: int, lesson_id: int)** - Оценки персоны за урок

- [x] /v2.0/persons/{person}/works/{work}/marks - **get_person_work_marks(person_id: int, work_id: int)** - Оценки персоны за работу

- [x] /v2.0/persons/{person}/subjects/{subject}/marks/{from}/{to} - **get_person_subject_marks(person_id: int, subject_id: int, start_time: datetime.datetime, end_time: datetime.datetime)** - Оценки персоны по предмету за период

- [x] /v2.0/persons/{person}/subject-groups/{subjectgroup}/marks/{from}/{to} - **func** - Оценки персоны по предмету за период

- [x] /v2.0/lessons/{date}/persons/{person}/marks - **func** - Оценки персоны по дате урока

- [x] /v2.0/persons/{person}/marks/{date} - **get_marks_by_date(person_id: int, date: datetime.datetime)** - Оценки персоны по дате выставления оценки

- [x] /v2.0/persons/{personId}/works/{workId}/mark - **get_person_work_marks(person_id: int, work_id: int)** - Выставить оценку ученику по работе

- [x] /v2.0/marks/values - **get_marks_values()** - Метод возвращает все поддерживаемые системы (типы) оценок и все возможные оценки в каждой из систем.
            
- [x] /v2.0/marks/values/type/{type} - **get_marks_values_by_type(marks_type: str)** - Метод возвращает все возможные оценки в запрашиваемой системе (типе) оценок. Чтобы узнать, какие типы поддерживаются нужно предварительно делать запрос marks/values без параметров.
 
- [x] /v2.0/persons - **func** - Список учеников в классе или учебной группе

- [x] /v2.0/edu-groups/{eduGroup}/students - **func** - Список учеников в классе или учебной группе

- [x] /v2.0/persons/search - **func** - 123

- [x] /v2.0/persons/{person} - **func** - Профиль персоны

- [x] /v2.0/persons/{person}/group/{group}/recentmarks - **func** - Последние оценки/отметки посещаемости персоны по предмету, указанному в параметре subject, начиная с даты определенном в параметре fromDate и с ограничением на выводимое количество указанном в параметре limit

- [x] /authorizations/esia/v2.0/regions - **func** - 123

- [x] /v2.0/edu-groups/{eduGroup}/reporting-periods - **func** - Список отчётных периодов для класса или учебной группы

- [x] /v2.0/edu-groups/{eduGroup}/reporting-period-group - **func** - Группа отчетных периодов для класса или учебной группы

- [x] /v2.0/persons/{person}/groups/{group}/schedules - **func** - Расписание ученика

- [x] /v2.0/school-rating/from/{from}/to/{to} - **func** - ѕолучение списка школ с наивысшим рейтингом за выбранный период

- [x] /v2.0/school-rating/from/{from}/to/{to}/new - **func** - ѕолучение списка новых школ с наивысшим рейтингом за выбранный период

- [x] /v2.0/schools/{school} - **func** - Профиль школы

- [x] /v2.0/schools - **func** - Список профилей нескольких школ (или список образовательных организаций пользователя, если не передано ни одного идентификатора школы)

- [x] /v2.0/schools/person-schools - **func** - Список образовательных организаций пользователя

- [x] /v2.0/schools/cities - **func** - Список населенных пунктов, образовательные организации которых включены в Систему

- [x] /v2.0/schools/search/by-oktmo - **func** - 123

- [x] /v2.0/schools/{school}/parameters - **func** - Параметры общеобразовательных организаций

- [x] /v2.0/events/{id}/invite - **func** - Пригласить в событие

- [x] /v2.0/groups/{id}/invite - **func** - Пригласить в группу

- [x] /v2.0/networks/{id}/invite - **func** - Пригласить в сеть

- [x] /v2.0/edu-groups/{eduGroup}/subjects - **func** - Список предметов, преподаваемых в классе в текущем отчётном периоде

- [x] /v2.0/schools/{school}/subjects - **func** - Список предметов, преподаваемых в образовательной организации в текущем учебном году

- [x] /v2.0/tasks/{task} - **func** - Домашнее задание

- [x] /v2.0/tasks - **func** - Домашние задания за несколько уроков

- [x] /v2.0/lessons/{lesson}/tasks - **func** - Список домашних заданий за урок

- [x] /v2.0/works/{work}/tasks - **func** - Список домашних заданий

- [x] /v2.0/persons/{person}/tasks - **func** - Список домашних заданий ученика по предмету

- [x] /v2.0/tasks/{personId}/undone - **func** - Список невыполненных домашних заданий обучающегося с истёкшим сроком выполнения

- [x] /v2.0/teacher/{teacher}/students - **func** - Список учеников для учителя который ведет уроки у этих учеников(они должны быть в расписании) от недели назад и на 30 дней вперед

- [x] /v2.0/schools/{school}/teachers - **func** - Список преподавателей в выбранной образовательной организации

- [x] /v2.0/edu-groups/{group}/teachers - **func** - Список учителей, которые ведут уроки в данной группе, учитываются уроки от недели назад и на 30 дней вперед

- [x] /v2.0/thematic-marks/{mark} - **func** - Получить оценку с заданным id

- [x] /v2.0/thematic-marks - **func** - Сохранить оценку

- [x] /v2.0/persons/{person}/edu-groups/{group}/subjects/{subject}/thematic-marks/{from}/{to} - **func** - Оценки персоны по предмету в учебной группе за период

- [x] /v2.0/persons/{person}/edu-groups/{group}/thematic-marks/{from}/{to} - **func** - Оценки персоны в учебной группе за период

- [x] /v2.0/persons/{person}/schools/{school}/thematic-marks/{from}/{to} - **func** - Оценки персоны в школе за период

- [x] /v2.0/edu-groups/{group}/subjects/{subject}/thematic-marks - **func** - Оценки в учебной группе по предмету

- [x] /v2.0/schools/{school}/timetables - **func** - Получение расписания школы

- [x] /v2.0/edu-groups/{eduGroup}/timetables - **func** - Получение расписания учебной группы

- [x] /v2.0/users/me/feed - **func** - Лента пользователя

- [x] /v2.0/users/{user}/groups - **func** - Список идентификаторов групп пользователя

- [ ] /v2.0/users/me/children - **func** - Список id пользователей детей текущего пользователя

- [ ] /v2.0/users/{user}/relatives - **func** - Получение всех родственных связей произвольного пользователя.

- [ ] /v2.0/users/me/relatives - **func** - Получение всех родственных связей текущего пользователя.

- [ ] /v2.0/users/me/childrenrelatives - **func** - Список id всех родственных связей детей произвольного пользователя

- [x] /v2.0/users/{user} - **func** - Профиль произвольного пользователя. Профиль текущего пользователя можно получить по users/me

- [x] /v2.0/users/me - **func** - Профиль текущего пользователя.

- [x] /v2.0/users/me/roles - **func** - Роли текущего пользователя.

- [x] /v2.0/users/many - **func** - Профили нескольких пользователей

- [x] /v2.0/users - **func** - Профили нескольких пользователей

- [x] /v2.0/users/{user}/roles - **func** - Роли пользователя

- [x] /v2.0/users/{user}/wallrecord - **func** - Отправить сообщение с изображением на стену пользователя

- [x] /v2.0/edu-groups/{group}/wa-marks/{from}/{to} - **func** - Средние взвешенные оценки учебной группы за период

- [x] /v2.0/works - **func** - Список работ на уроке

- [x] /v2.0/lessons/{lesson}/works - **func** - Список работ на уроке

- [x] /v2.0/works/{work} - **func** - Работа на уроке

- [x] /v2.0/works/many - **func** - Получение списка работ по списку id

- [x] /v2.0/works/{work}/persons/{person}/status - **func** - Изменить статус выполнения домашней работы учащимся.

- [x] /v2.0/work-types/{school} - **func** - Получение списка всех типов работ школы
