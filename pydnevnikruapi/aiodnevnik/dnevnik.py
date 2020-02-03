import datetime

import aiohttp
import requests
from pydnevnikruapi.aiodnevnik.exceptions import AsyncDiaryError


class AsyncDiaryBase:
    """
    Базовый класс для асинхронного использования дневник.ру API
    """
    def __init__(self, login: str = None, password: str = None, token: str = None):
        self.token = token
        if token is None:
            self.token = self.get_token()

        self.login = login
        self.password = password
        self.session = aiohttp.ClientSession()
        self.host = "https://api.dnevnik.ru/v2/"

    def get_token(self):
        token_info = requests.post(
            "https://api.dnevnik.ru/v2/authorizations/bycredentials",
            json={
                "client_id": "1d7bd105-4cd1-4f6c-9ecc-394e400b53bd",
                "client_secret": "5dcb5237-b5d3-406b-8fee-4441c3a66c99",
                "username": self.login,
                "password": self.password,
                "scope": "Schools,Relatives,EduGroups,Lessons,marks,EduWorks,Avatar,"
                "EducationalInfo,CommonInfo,ContactInfo,FriendsAndRelatives,"
                "Files,Wall,Messages",
            },
        )
        if token_info.status_code in [500, 502]:
            raise AsyncDiaryError(
                "Сайт лежит или ведутся технические работы, использование api временно невозможно"
            )
        token = token_info.json()
        if token.get("type") == "authorizationFailed":
            raise AsyncDiaryError(token["description"])
        if token.get("type") == "maxAttempsExceeded":
            raise AsyncDiaryError(token["description"])

        self.token = token["accessToken"]
        return token["accessToken"]

    async def close_session(self):
        await self.session.close()

    @staticmethod
    async def _check_response(response):
        if response.content_type == "text/html":
            error_html = await response.text()
            error_text = " ".join(
                word
                for word in error_html.split('<div class="error__description">')[-1]
                .split("<p>")[1]
                .strip()[:-4]
                .split()
            )
            raise AsyncDiaryError(error_text)
        json_response = await response.json()
        if isinstance(json_response, dict):
            if json_response.get("type") == "apiUnknownError":
                raise AsyncDiaryError(
                    "Незвестная ошибка API, проверьте правильность параметров"
                )
            if json_response.get("type") == "apiServerError":
                raise AsyncDiaryError(
                    "Неизвестная ошибка в API, проверьте правильность параметров"
                )
            if json_response.get("type") == "parameterInvalid":
                raise AsyncDiaryError(json_response["description"])
        elif isinstance(json_response, list):
            # TODO strange list response errors
            pass

    async def get(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}

        async with self.session.get(
            self.host + method,
            params=params,
            headers={"Access-Token": self.token},
            **kwargs,
        ) as response:
            await self._check_response(response)
            json_response = await response.json()
        return json_response

    async def post(self, method: str, data=None, **kwargs):
        if data is None:
            data = {}
        async with self.session.post(
            self.host + method,
            json=data,  # json or data?
            headers={"Access-Token": self.token},
            **kwargs,
        ) as response:
            await self._check_response(response)
            json_response = await response.json()
        return json_response

    async def delete(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}

        async with self.session.delete(
            self.host + method,
            params=params,
            headers={"Access-Token": self.token},
            **kwargs,
        ) as response:
            await self._check_response(response)
            json_response = await response.json()
        return json_response

    async def put(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}

        async with self.session.put(
            self.host + method,
            data=params,
            headers={"Access-Token": self.token},
            **kwargs,
        ) as response:
            await self._check_response(response)
            json_response = await response.json()
        return json_response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()


class AsyncDiaryAPI(AsyncDiaryBase):
    """
    Класс для асинхронного использования дневник.ру API
    """
    def __init__(self, login: str = None, password: str = None, token: str = None):
        self.login = login
        self.password = password

        super().__init__(login, password, token)

    async def get_school(self):
        school_id = await self.get("schools/person-schools")
        return school_id

    async def get_info(self):
        user_id = await self.get("users/me")
        return user_id

    async def get_classmates(self):
        classmates = await self.get(f"users/me/classmates")
        return classmates

    async def get_context(self):
        context = await self.get(f"users/me/context")
        return context

    async def get_organizations(self):
        organizations = await self.get(f"users/me/organizations")
        return organizations

    async def get_organization_info(self, organization_id: int):
        organization_info = await self.get(f"users/me/organizations/{organization_id}")
        return organization_info

    async def get_user_context(self, user_id: int):
        #  TODO: check strange response
        context = await self.get(f"users/{user_id}/context")
        return context

    async def get_user_memberships(self, user_id: int):
        memberships = await self.get(f"users/{user_id}/school-memberships")
        return memberships

    async def get_user_education(self, user_id: int):
        education = await self.get(f"users/{user_id}/education")
        return education

    async def get_person_memberships(self, person_id: int):
        memberships = await self.get(f"persons/{person_id}/school-memberships")
        return memberships

    async def get_schools(self):
        schools = await self.get(f"users/me/schools")
        return schools

    async def get_user_schools(self, user_id: int):
        schools = await self.get(f"users/{user_id}/schools")
        return schools

    async def get_edu_groups(self):
        edu_groups = await self.get(f"users/me/edu-groups")
        return edu_groups

    async def get_user_edu_groups(self, user_id: int):
        edu_groups = await self.get(f"users/{user_id}/edu-groups")
        return edu_groups

    async def get_memberships(self):
        schools_memberships = await self.get(f"users/me/school-memberships")
        return schools_memberships

    async def get_group_info(self, edu_group_id: int):
        edu_group_info = await self.get(f"edu-groups/{edu_group_id}")
        return edu_group_info

    async def get_groups_info(self, edu_groups_list: list):
        edu_groups_info = await self.get(
            f"edu-groups", params={"eduGroups": edu_groups_list}
        )
        return edu_groups_info

    async def get_school_groups(self, school_id: int):
        school_edu_groups = await self.get(f"schools/{school_id}/edu-groups")
        return school_edu_groups

    async def get_person_groups(self, person_id: int):
        person_edu_groups = await self.get(f"persons/{person_id}/edu-groups")
        return person_edu_groups

    async def get_students_groups_list(self):
        students_groups_list = await self.get(f"edu-groups/students")
        return students_groups_list

    async def get_person_groups_all(self, person_id: int):
        person_edu_all = await self.get(f"persons/{person_id}/edu-groups/all")
        return person_edu_all

    async def get_person_school_groups(self, person_id: int, school_id: int):
        person_edu_groups_in_school = await self.get(
            f"persons/{person_id}/schools/{school_id}/edu-groups"
        )
        return person_edu_groups_in_school

    async def get_groups_pupils(self, edu_group_id: int):
        edu_groups_list = await self.get(f"edu-groups/{edu_group_id}/persons")
        return edu_groups_list

    async def get_groups_parallel(self, group_id: int):
        edu_groups_list = await self.get(f"edu-groups/{group_id}/parallel")
        return edu_groups_list

    async def get_group_marks(self, group_id: int):
        edu_groups_marks = await self.get(f"edu-groups/{group_id}/final-marks")
        return edu_groups_marks

    async def get_person_group_marks(self, person_id: int, group_id: int):
        #  TODO: check strange response
        person_marks_in_group = await self.get(
            f"persons/{person_id}/edu-groups/{group_id}/final-marks"
        )
        return person_marks_in_group

    async def get_person_group_marks_final(self, person_id: int, group_id: int):
        person_final_marks_in_group = await self.get(
            f"persons/{person_id}/edu-groups/{group_id}/allfinalmarks"
        )
        return person_final_marks_in_group

    async def get_group_subject_final_marks(self, group_id: int, subject_id: int):
        group_subject_marks = await self.get(
            f"edu-groups/{group_id}/subjects/{subject_id}/final-marks"
        )
        return group_subject_marks

    async def get_friends(self):
        my_friends = await self.get(f"users/me/friends")
        return my_friends

    async def get_user_friends(self, user_id: int):
        user_friends = await self.get(f"users/{user_id}/friends")
        return user_friends

    async def get_school_homework(
        self,
        school_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        homework = await self.get(
            f"users/me/school/{school_id}/homeworks",
            params={"startDate": start_time, "endDate": end_time},
        )
        return homework

    async def get_homework_by_id(self, homework_id: int):
        homework = await self.get(
            f"users/me/school/homeworks", params={"homeworkId": homework_id}
        )
        return homework

    async def get_person_homework(
        self,
        school_id: int,
        person_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        homework = await self.get(
            f"persons/{person_id}/school/{school_id}/homeworks",
            params={"startDate": start_time, "endDate": end_time},
        )
        return homework

    async def delete_lesson_log(self, lesson_id: int, person_id: int):
        response = await self.delete(
            f"lessons/{lesson_id}/log-entries", params={"person": person_id}
        )
        return response

    async def get_lesson_log(self, lesson_id: int):
        lesson_log = await self.get(f"lessons/{lesson_id}/log-entries")
        return lesson_log

    async def post_lesson_log(self, lesson_id: int, lesson_log_entry: str):
        """
        lesson_log_entry example:
        {
            "person": 0,
            "lesson": 0,
            "person_str": "string",
            "lesson_str": "string",
            "comment": "string",
            "status": "string",
            "createdDate": "2019-09-15T16:35:53.853Z"
        }

        """
        lesson_log = await self.post(
            f"lessons/{lesson_id}/log-entries",
            data={"lessonLogEntry": lesson_log_entry},
        )
        return lesson_log

    async def put_lesson_log(
        self, lesson_id: int, person_id: int, lesson_log_entry: str
    ):
        """
                lesson_log_entry example:
                {
                    "person": 0,
                    "lesson": 0,
                    "person_str": "string",
                    "lesson_str": "string",
                    "comment": "string",
                    "status": "string",
                    "createdDate": "2019-09-15T16:35:53.853Z"
                }

                """
        lesson_log = await self.put(
            f"lessons/{lesson_id}/log-entries",
            data={"person": person_id, "lessonLogEntry": lesson_log_entry},
        )
        return lesson_log

    async def get_lesson_logs(self, lessons_ids: list):
        lesson_logs = await self.get(
            f"lesson-log-entries", params={"lessons": lessons_ids}
        )
        return lesson_logs

    async def get_person_lesson_log(self, person_id: int, lesson_id: int):
        lesson_logs = await self.get(
            f"lesson-log-entries/lesson/{lesson_id}/person/{person_id}"
        )
        return lesson_logs

    async def get_group_lesson_log(
        self,
        group_id: int,
        subject_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        lesson_logs = await self.get(
            f"lesson-log-entries/group/{group_id}",
            params={"subject": subject_id, "from": start_time, "to": end_time},
        )
        return lesson_logs

    async def get_person_subject_lesson_log(
        self,
        person_id: int,
        subject_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        lesson_logs = await self.get(
            f"lesson-log-entries/person/{person_id}/subject/{subject_id}",
            params={"subject": subject_id, "from": start_time, "to": end_time},
        )
        return lesson_logs

    async def get_person_lesson_logs(
        self,
        person_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        lesson_logs = await self.get(
            f"persons/{person_id}/lesson-log-entries",
            params={"startDate": start_time, "endDate": end_time},
        )
        return lesson_logs

    async def get_lesson_log_statuses(self):
        lesson_logs_statuses = self.get(f"lesson-log-entries/statuses")
        return lesson_logs_statuses

    async def get_lesson_info(self, lesson_id: int):
        lesson_info = await self.get(f"lessons/{lesson_id}")
        return lesson_info

    async def get_many_lessons_info(self, lessons_list: list):
        lesson_info = await self.post(f"lessons/many", data={"lessons": lessons_list})
        return lesson_info

    async def get_group_lessons_info(
        self,
        group_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        lessons_info = await self.get(
            f"edu-groups/{group_id}/lessons/{start_time}/{end_time}"
        )
        return lessons_info

    async def get_marks_histogram(self, work_id: int):
        marks_histogram = await self.get(f"works/{work_id}/marks/histogram")
        return marks_histogram

    async def get_subject_marks_histogram(
        self, group_id: int, period_id: int, subject_id: int
    ):
        marks_histogram = await self.get(
            f"periods/{period_id}/subjects/{subject_id}/groups/{group_id}/marks/histogram"
        )
        return marks_histogram

    async def get_mark_by_id(self, mark_id: int):
        mark_info = await self.get(f"marks/{mark_id}")
        return mark_info

    async def get_marks_by_work(self, work_id: int):
        marks = await self.get(f"works/{work_id}/marks")
        return marks

    async def get_marks_by_lesson(self, lesson_id: int):
        marks = await self.get(f"lessons/{lesson_id}/marks")
        return marks

    async def get_marks_by_lessons(self, lessons_ids: list):
        marks = await self.post(f"lessons/marks", data={"lessons": lessons_ids})
        return marks

    async def get_group_marks_period(
        self,
        group_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        marks = await self.get(f"edu-groups/{group_id}/marks/{start_time}/{end_time}")
        return marks

    async def get_group_subject_marks(
        self,
        group_id: int,
        subject_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        marks = await self.get(
            f"edu-groups/{group_id}/subjects/{subject_id}/marks/{start_time}/{end_time}"
        )
        return marks

    async def get_person_marks(
        self,
        person_id: int,
        school_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        marks = await self.get(
            f"persons/{person_id}/schools/{school_id}/marks/{start_time}/{end_time}"
        )
        return marks

    async def get_person_lessons_marks(self, person_id: int, lesson_id: int):
        marks = await self.get(f"persons/{person_id}/lessons/{lesson_id}/marks")
        return marks

    async def get_person_work_marks(self, person_id: int, work_id: int):
        marks = self.get(f"persons/{person_id}/works/{work_id}/marks")
        return marks

    async def get_person_subject_marks(
        self,
        person_id: int,
        subject_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        marks = await self.get(
            f"persons/{person_id}/subjects/{subject_id}/marks/{start_time}/{end_time}"
        )
        return marks

    async def get_marks_by_date(self, person_id: int, date=datetime.datetime.now()):
        marks = await self.get(f"persons/{person_id}/marks/{date}")
        return marks

    async def get_marks_values(self):
        marks_values = await self.get(f"https://api.dnevnik.ru/v2.0/marks/values")
        return marks_values

    async def get_marks_values_by_type(self, marks_type: str):
        marks_values = await self.get(f"marks/values/type/{marks_type}")
        return marks_values

    async def get_person_average_marks(self, person: int, period: int):
        marks = await self.get(f"persons/{person}/reporting-periods/{period}/avg-mark")
        return marks

    async def get_person_average_marks_by_subject(
        self, person_id: int, period: int, subject_id: int
    ):
        marks = await self.get(
            f"persons/{person_id}/reporting-periods/{period}/subjects/{subject_id}/avg-mark"
        )
        return marks

    async def get_group_average_marks_by_date(
        self,
        group_id: int,
        period: int,
        date: datetime.datetime = datetime.datetime.now(),
    ):
        marks = await self.get(
            f"edu-groups/{group_id}/reporting-periods/{period}/avg-marks/{date}"
        )
        return marks

    async def get_group_average_marks_by_time(
        self,
        group_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        marks = await self.get(
            f"edu-groups/{group_id}/avg-marks/{start_time}/{end_time}"
        )
        return marks

    async def get_final_group_marks(self, group_id: int):
        marks = await self.get(f"edu-group/{group_id}/criteria-marks-totals")
        return marks

    async def get_final_group_marks_by_subject(self, group_id: int, subject_id: int):
        marks = await self.get(
            f"edu-group/{group_id}/subject/{subject_id}/criteria-marks-totals"
        )
        return marks

    async def get_group_persons(self, group_id: int):
        persons = await self.get(f"persons", params={"eduGroup": group_id})
        return persons

    async def get_person_info(self, person_id: int):
        person_info = await self.get(f"persons/{person_id}")
        return person_info

    async def get_recent_person_marks(self, person_id: int, group_id: int):
        recent_person_marks = await self.get(
            f"persons/{person_id}/group/{group_id}/recentmarks"
        )
        return recent_person_marks

    async def get_group_reports(self, group_id: int):
        group_reports = await self.get(f"edu-groups/{group_id}/reporting-periods")
        return group_reports

    async def get_person_schedule(
        self,
        person_id,
        group_id,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        person_schedule = await self.get(
            f"https://api.dnevnik.ru/v2.0/persons/{person_id}/groups/{group_id}/schedules",
            params={"startDate": start_time, "endDate": end_time},
        )
        return person_schedule

    async def get_best_schools(
        self,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        best_schools = await self.get(f"school-rating/from/{start_time}/to/{end_time}")
        return best_schools

    async def get_school_profile(self, school_id: int):
        school_profile = await self.get(f"schools/{school_id}")
        return school_profile

    async def get_schools_profiles(self, schools_ids: list):
        school_profiles = await self.get(f"schools", params={"schools": schools_ids})
        return school_profiles

    async def get_my_schools(self):
        person_schools = await self.get(f"schools/person-schools")
        return person_schools

    async def get_all_schools(self):
        all_schools = await self.get(f"schools/cities")
        return all_schools

    async def get_school_params(self, school_id: int):
        school_params = await self.get(f"schools/{school_id}/parameters")
        return school_params

    async def get_group_subjects(self, group_id: int):
        group_subjects = await self.get(f"edu-groups/{group_id}/subjects")
        return group_subjects

    async def get_school_subjects(self, school_id: int):
        school_subjects = await self.get(f"schools/{school_id}/subjects")
        return school_subjects

    async def get_task_info(self, task_id: int):
        task_info = await self.get(f"tasks/{task_id}")
        return task_info

    async def get_lessons_task(self, lessons_ids: list):
        lessons_task = await self.get(f"tasks", params={"lessons": lessons_ids})
        return lessons_task

    async def get_lesson_task(self, lesson_id: int):
        lesson_task = await self.get(f"lessons/{lesson_id}/tasks")
        return lesson_task

    async def get_person_tasks(
        self,
        person_id: int,
        subject_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        person_subject_tasks = await self.get(
            f"persons/{person_id}/tasks",
            params={"subject": subject_id, "from": start_time, "to": end_time},
        )
        return person_subject_tasks

    async def get_teacher_students(self, teacher_id: int):
        teacher_students = await self.get(f"teacher/{teacher_id}/students")
        return teacher_students

    async def get_school_teachers(self, school_id: int):
        school_teachers = await self.get(f"schools/{school_id}/teachers")
        return school_teachers

    async def get_school_timetable(self, school_id: int):
        school_timetable = await self.get(f"schools/{school_id}/timetables")
        return school_timetable

    async def get_group_timetable(self, group_id: int):
        group_timetable = await self.get(f"edu-groups/{group_id}/timetables")
        return group_timetable

    async def get_feed(self):
        my_feed = await self.get(
            f"users/me/feed", params={"date": str(datetime.datetime.now())}
        )
        return my_feed

    async def get_user_groups(self, user_id: int):
        user_groups = await self.get(f"users/{user_id}/groups")
        return user_groups

    async def get_person_children(self, person_id: int):
        person_children = await self.get(f"user/{person_id}/children")
        return person_children

    async def get_user_children(self, user_id: int):
        children = await self.get(f"user/{user_id}/children")
        return children

    async def get_children(self):
        my_children = await self.get(f"users/me/children")
        return my_children

    async def get_user_relatives(self, user_id: int):
        user_rel = await self.get(f"users/{user_id}/relatives")
        return user_rel

    async def get_relatives(self):
        my_rel = await self.get(f"users/me/relatives")
        return my_rel

    async def get_children_relatives(self):
        my_children_relatives = await self.get(f"users/me/childrenrelatives")
        return my_children_relatives

    async def get_user_info(self, user_id: int):
        user_info = await self.get(f"users/{user_id}")
        return user_info

    async def get_roles(self):
        my_roles = await self.get(f"users/me/roles")
        return my_roles

    async def get_user_roles(self, user_id: int):
        user_roles = await self.get(f"users/{user_id}/roles")
        return user_roles

    async def get_group_average_marks(
        self,
        group_id: int,
        start_time: str = str(datetime.datetime.now()),
        end_time: str = str(datetime.datetime.now()),
    ):
        weighted_group_average_marks = await self.get(
            f"edu-groups/{group_id}/wa-marks/{start_time}/{end_time}"
        )
        return weighted_group_average_marks

    async def get_lesson_works(self, lesson_id: int):
        lesson_works = await self.get(f"works", params={"lesson": lesson_id})
        return lesson_works

    async def create_lesson_work(self, work: str):
        """
        work example:

                {
          "id": 0,
          "id_str": "string",
          "type": 0,
          "workType": 0,
          "markType": "string",
          "markCount": 0,
          "lesson": 0,
          "lesson_str": "string",
          "displayInJournal": true,
          "status": "string",
          "eduGroup": 0,
          "eduGroup_str": "string",
          "tasks": [
            {
              "id": 0,
              "id_str": "string",
              "person": 0,
              "person_str": "string",
              "work": 0,
              "work_str": "string",
              "status": "string",
              "targetDate": "2019-09-15T16:35:54.384Z"
            }
          ],
          "text": "string",
          "periodNumber": 0,
          "periodType": "string",
          "subjectId": 0,
          "isImportant": true,
          "targetDate": "2019-09-15T16:35:54.384Z",
          "sentDate": "2019-09-15T16:35:54.384Z",
          "createdBy": 0,
          "files": [
            0
          ],
          "oneDriveLinks": [
            0
          ]
        }
        """
        lesson_works = await self.post(f"works", data={"work": work})
        return lesson_works

    async def get_work_types(self, school_id: int):
        work_types = await self.get(f"work-types/{school_id}")
        return work_types

    async def invite_to_event(self, invite_id: int):
        response = await self.post(f"events/{invite_id}/invite ")
        return response
