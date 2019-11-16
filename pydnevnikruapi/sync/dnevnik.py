import requests
import datetime
from pydnevnikruapi.sync.exceptions import DiaryError


class DiaryBase:
    def __init__(self, login: str = None, password: str = None, token: str = None):
        self.session = requests.Session()
        self.host = "https://api.dnevnik.ru/v2/"
        if token is None:
            self.token = self.get_token(login, password)
        else:
            self.token = token
        self.session.headers = {"Access-Token": self.token}

    def get_token(self, login, password):
        token = self.session.post(
            "https://api.dnevnik.ru/v2/authorizations/bycredentials",
            json={
                "client_id": "1d7bd105-4cd1-4f6c-9ecc-394e400b53bd",
                "client_secret": "5dcb5237-b5d3-406b-8fee-4441c3a66c99",
                "username": login,
                "password": password,
                "scope": "Schools,Relatives,EduGroups,Lessons,marks,EduWorks,Avatar,"
                "EducationalInfo,CommonInfo,ContactInfo,FriendsAndRelatives,"
                "Files,Wall,Messages",
            },
        )
        json_token = token.json()
        if json_token.get("type") == "authorizationFailed":
            raise DiaryError(json_token["description"])
        elif token.status_code != 200:
            raise DiaryError(
                "Сайт лежит или ведутся технические работы, использование api временно невозможно"
            )
        else:
            return json_token["accessToken"]

    @staticmethod
    def _check_response(response):
        if response.headers.get("Content-Type") == "text/html":
            error_html = response.content.decode()
            error_text = " ".join(
                word
                for word in error_html.split('<div class="error__description">')[-1]
                .split("<p>")[1]
                .strip()[:-4]
                .split()
            )
            raise DiaryError(error_text)
        json_response = response.json()
        if isinstance(json_response, dict):
            if json_response.get("type") == "parameterInvalid":
                raise DiaryError(json_response["description"])
            elif json_response.get("type") == "apiServerError":
                raise DiaryError(
                    "Неизвестная ошибка в API, проверьте правильность параметров"
                )
            elif json_response.get("type") == "apiUnknownError":
                raise DiaryError(
                    "Неизвестная ошибка в API, проверьте правильность параметров"
                )

    def get(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}
        response = self.session.get(self.host + method, params=params, **kwargs)
        self._check_response(response)
        return response.json()

    def post(self, method: str, data=None, **kwargs):
        if data is None:
            data = {}
        response = self.session.post(self.host + method, data=data, **kwargs)
        self._check_response(response)
        return response.json()

    def delete(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}
        response = self.session.delete(self.host + method, params=params, **kwargs)
        self._check_response(response)
        return response.json()

    def put(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}
        response = self.session.put(self.host + method, data=params, **kwargs)
        self._check_response(response)
        return response.json()


class DiaryAPI:
    def __init__(self, login: str = None, password: str = None, token: str = None):
        if token is None:
            self.api = DiaryBase(login=login, password=password)
        else:
            self.api = DiaryBase(token=token)

    def get_token(self):
        return self.api.token

    def get_school(self):
        school_id = self.api.get("schools/person-schools")
        return school_id

    def get_info(self):
        user_id = self.api.get("users/me")
        return user_id

    def get_classmates(self):
        classmates = self.api.get(f"users/me/classmates")
        return classmates

    def get_context(self):
        context = self.api.get(f"users/me/context")
        return context

    def get_organizations(self):
        organizations = self.api.get(f"users/me/organizations")
        return organizations

    def get_organization_info(self, organization_id: int):
        organization_info = self.api.get(f"users/me/organizations/{organization_id}")
        return organization_info

    def get_user_context(self, user_id: int):
        #  TODO: check strange response
        context = self.api.get(f"users/{user_id}/context")
        return context

    def get_user_memberships(self, user_id: int):
        memberships = self.api.get(f"users/{user_id}/school-memberships")
        return memberships

    def get_user_education(self, user_id: int):
        education = self.api.get(f"users/{user_id}/education")
        return education

    def get_person_memberships(self, person_id: int):
        memberships = self.api.get(f"persons/{person_id}/school-memberships")
        return memberships

    def get_schools(self):
        schools = self.api.get(f"users/me/schools")
        return schools

    def get_user_schools(self, user_id: int):
        schools = self.api.get(f"users/{user_id}/schools")
        return schools

    def get_edu_groups(self):
        edu_groups = self.api.get(f"users/me/edu-groups")
        return edu_groups

    def get_user_edu_groups(self, user_id: int):
        edu_groups = self.api.get(f"users/{user_id}/edu-groups")
        return edu_groups

    def get_memberships(self):
        schools_memberships = self.api.get(f"users/me/school-memberships")
        return schools_memberships

    def get_group_info(self, edu_group_id: int):
        edu_group_info = self.api.get(f"edu-groups/{edu_group_id}")
        return edu_group_info

    def get_groups_info(self, edu_groups_list: list):
        edu_groups_info = self.api.get(
            f"edu-groups", params={"eduGroups": edu_groups_list}
        )
        return edu_groups_info

    def get_school_groups(self, school_id: int):
        school_edu_groups = self.api.get(f"schools/{school_id}/edu-groups")
        return school_edu_groups

    def get_person_groups(self, person_id: int):
        person_edu_groups = self.api.get(f"persons/{person_id}/edu-groups")
        return person_edu_groups

    def get_person_groups_all(self, person_id: int):
        person_edu_all = self.api.get(f"persons/{person_id}/edu-groups/all")
        return person_edu_all

    def get_person_school_groups(self, person_id: int, school_id: int):
        person_edu_groups_in_school = self.api.get(
            f"persons/{person_id}/schools/{school_id}/edu-groups"
        ).json()
        return person_edu_groups_in_school

    def get_groups_pupils(self, edu_group_id: int):
        edu_groups_list = self.api.get(f"edu-groups/{edu_group_id}/persons")
        return edu_groups_list

    def get_groups_parallel(self, group_id: int):
        edu_groups_list = self.api.get(f"edu-groups/{group_id}/parallel")
        return edu_groups_list

    def get_group_marks(self, group_id: int):
        edu_groups_marks = self.api.get(f"edu-groups/{group_id}/final-marks")
        return edu_groups_marks

    def get_person_group_marks(self, person_id: int, group_id: int):
        #  TODO: check strange response
        person_marks_in_group = self.api.get(
            f"persons/{person_id}/edu-groups/{group_id}/final-marks"
        )
        return person_marks_in_group

    def get_person_group_marks_final(self, person_id: int, group_id: int):
        person_final_marks_in_group = self.api.get(
            f"persons/{person_id}/edu-groups/{group_id}/allfinalmarks"
        )
        return person_final_marks_in_group

    def get_group_subject_final_marks(self, group_id: int, subject_id: int):
        group_subject_marks = self.api.get(
            f"edu-groups/{group_id}/subjects/{subject_id}/final-marks"
        )
        return group_subject_marks

    def get_friends(self):
        my_friends = self.api.get(f"users/me/friends")
        return my_friends

    def get_user_friends(self, user_id: int):
        user_friends = self.api.get(f"users/{user_id}/friends")
        return user_friends

    def get_school_homework(
        self,
        school_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        homework = self.api.get(
            f"users/me/school/{school_id}/homeworks",
            params={"startDate": start_time, "endDate": end_time},
        )
        return homework

    def get_homework_by_id(self, homework_id: int):
        homework = self.api.get(
            f"users/me/school/homeworks", params={"homeworkId": homework_id}
        )
        return homework

    def get_person_homework(
        self,
        school_id: int,
        person_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        homework = self.api.get(
            f"persons/{person_id}/school/{school_id}/homeworks",
            params={"startDate": start_time, "endDate": end_time},
        )
        return homework

    def delete_lesson_log(self, lesson_id: int, person_id: int):
        response = self.api.delete(
            f"lessons/{lesson_id}/log-entries", params={"person": person_id}
        )
        return response

    def get_lesson_log(self, lesson_id: int):
        lesson_log = self.api.get(f"lessons/{lesson_id}/log-entries")
        return lesson_log

    def post_lesson_log(self, lesson_id: int, lesson_log_entry: str):
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
        lesson_log = self.api.post(
            f"lessons/{lesson_id}/log-entries",
            data={"lessonLogEntry": lesson_log_entry},
        )
        return lesson_log

    def put_lesson_log(self, lesson_id: int, person_id: int, lesson_log_entry: str):
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
        lesson_log = self.api.put(
            f"lessons/{lesson_id}/log-entries",
            data={"person": person_id, "lessonLogEntry": lesson_log_entry},
        )
        return lesson_log

    def get_lesson_logs(self, lessons_ids: list):
        lesson_logs = self.api.get(
            f"lesson-log-entries", params={"lessons": lessons_ids}
        )
        return lesson_logs

    def get_person_lesson_log(self, person_id: int, lesson_id: int):
        lesson_logs = self.api.get(
            f"lesson-log-entries/lesson/{lesson_id}/person/{person_id}"
        )
        return lesson_logs

    def get_group_lesson_log(
        self,
        group_id: int,
        subject_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        lesson_logs = self.api.get(
            f"lesson-log-entries/group/{group_id}",
            params={"subject": subject_id, "from": start_time, "to": end_time},
        )
        return lesson_logs

    def get_person_subject_lesson_log(
        self,
        person_id: int,
        subject_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        lesson_logs = self.api.get(
            f"lesson-log-entries/person/{person_id}/subject/{subject_id}",
            params={"subject": subject_id, "from": start_time, "to": end_time},
        )
        return lesson_logs

    def get_person_lesson_logs(
        self,
        person_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        lesson_logs = self.api.get(
            f"persons/{person_id}/lesson-log-entries",
            params={"startDate": start_time, "endDate": end_time},
        )
        return lesson_logs

    def get_lesson_log_statuses(self):
        lesson_logs_statuses = self.api.get(f"lesson-log-entries/statuses").json()
        return lesson_logs_statuses

    def get_lesson_info(self, lesson_id: int):
        lesson_info = self.api.get(f"lessons/{lesson_id}").json()
        return lesson_info

    def get_many_lessons_info(self, lessons_list: list):
        lesson_info = self.api.post(f"lessons/many", data={"lessons": lessons_list})
        return lesson_info

    def get_group_lessons_info(
        self,
        group_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        lessons_info = self.api.get(
            f"edu-groups/{group_id}/lessons/{start_time}/{end_time}"
        )
        return lessons_info

    def get_marks_histogram(self, work_id: int):
        marks_histogram = self.api.get(f"works/{work_id}/marks/histogram").json()
        return marks_histogram

    def get_subject_marks_histogram(
        self, group_id: int, period_id: int, subject_id: int
    ):
        marks_histogram = self.api.get(
            f"periods/{period_id}/subjects/{subject_id}/groups/{group_id}/marks/histogram"
        )
        return marks_histogram

    def get_mark_by_id(self, mark_id: int):
        mark_info = self.api.get(f"marks/{mark_id}")
        return mark_info

    def get_marks_by_work(self, work_id: int):
        marks = self.api.get(f"works/{work_id}/marks")
        return marks

    def get_marks_by_lesson(self, lesson_id: int):
        marks = self.api.get(f"lessons/{lesson_id}/marks")
        return marks

    def get_marks_by_lessons(self, lessons_ids: list):
        marks = self.api.post(f"lessons/marks", data={"lessons": lessons_ids})
        return marks

    def get_group_marks_period(
        self,
        group_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        marks = self.api.get(f"edu-groups/{group_id}/marks/{start_time}/{end_time}")
        return marks

    def get_group_subject_marks(
        self,
        group_id: int,
        subject_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        marks = self.api.get(
            f"edu-groups/{group_id}/subjects/{subject_id}/marks/{start_time}/{end_time}"
        )
        return marks

    def get_person_marks(
        self,
        person_id: int,
        school_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        marks = self.api.get(
            f"persons/{person_id}/schools/{school_id}/marks/{start_time}/{end_time}"
        )
        return marks

    def get_person_lessons_marks(self, person_id: int, lesson_id: int):
        marks = self.api.get(f"persons/{person_id}/lessons/{lesson_id}/marks")
        return marks

    def get_person_work_marks(self, person_id: int, work_id: int):
        marks = self.api.get(f"persons/{person_id}/works/{work_id}/marks")
        return marks

    def get_person_subject_marks(
        self,
        person_id: int,
        subject_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        marks = self.api.get(
            f"persons/{person_id}/subjects/{subject_id}/marks/{start_time}/{end_time}"
        )
        return marks

    def get_marks_by_date(
        self, person_id: int, date: datetime.datetime = datetime.datetime.now()
    ):
        marks = self.api.get(f"persons/{person_id}/marks/{date}")
        return marks

    def get_marks_values(self):
        marks_values = self.api.get(f"https://api.dnevnik.ru/v2.0/marks/values")
        return marks_values

    def get_marks_values_by_type(self, marks_type: str):
        marks_values = self.api.get(f"marks/values/type/{marks_type}")
        return marks_values

    def get_person_average_marks(self, person: int, period: int):
        marks = self.api.get(f"persons/{person}/reporting-periods/{period}/avg-mark")
        return marks

    def get_person_average_marks_by_subject(
        self, person_id: int, period: int, subject_id: int
    ):
        marks = self.api.get(
            f"persons/{person_id}/reporting-periods/{period}/subjects/{subject_id}/avg-mark"
        )
        return marks

    def get_group_average_marks_by_date(
        self,
        group_id: int,
        period: int,
        date: datetime.datetime = datetime.datetime.now(),
    ):
        marks = self.api.get(
            f"edu-groups/{group_id}/reporting-periods/{period}/avg-marks/{date}"
        )
        return marks

    def get_group_average_marks_by_time(
        self,
        group_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        marks = self.api.get(f"edu-groups/{group_id}/avg-marks/{start_time}/{end_time}")
        return marks

    def get_final_group_marks(self, group_id: int):
        marks = self.api.get(f"edu-group/{group_id}/criteria-marks-totals")
        return marks

    def get_final_group_marks_by_subject(self, group_id: int, subject_id: int):
        marks = self.api.get(
            f"edu-group/{group_id}/subject/{subject_id}/criteria-marks-totals"
        )
        return marks

    def get_group_persons(self, group_id: int):
        persons = self.api.get(f"persons", params={"eduGroup": group_id})
        return persons

    def get_person_info(self, person_id: int):
        person_info = self.api.get(f"persons/{person_id}")
        return person_info

    def get_recent_person_marks(self, person_id: int, group_id: int):
        recent_person_marks = self.api.get(
            f"persons/{person_id}/group/{group_id}/recentmarks"
        )
        return recent_person_marks

    def get_group_reports(self, group_id: int):
        group_reports = self.api.get(f"edu-groups/{group_id}/reporting-periods")
        return group_reports

    def get_person_schedule(
        self,
        person_id,
        group_id,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        person_schedule = self.api.get(
            f"https://api.dnevnik.ru/v2.0/persons/{person_id}/groups/{group_id}/schedules",
            params={"startDate": start_time, "endDate": end_time},
        )
        return person_schedule

    def get_best_schools(
        self,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        best_schools = self.api.get(f"school-rating/from/{start_time}/to/{end_time}")
        return best_schools

    def get_school_profile(self, school_id: int):
        school_profile = self.api.get(f"schools/{school_id}")
        return school_profile

    def get_schools_profiles(self, schools_ids: list):
        school_profiles = self.api.get(f"schools", params={"schools": schools_ids})
        return school_profiles

    def get_my_schools(self):
        person_schools = self.api.get(f"schools/person-schools")
        return person_schools

    def get_all_schools(self):
        all_schools = self.api.get(f"schools/cities")
        return all_schools

    def get_school_params(self, school_id: int):
        school_params = self.api.get(f"schools/{school_id}/parameters")
        return school_params

    def get_group_subjects(self, group_id: int):
        group_subjects = self.api.get(f"edu-groups/{group_id}/subjects")
        return group_subjects

    def get_school_subjects(self, school_id: int):
        school_subjects = self.api.get(f"schools/{school_id}/subjects")
        return school_subjects

    def get_task_info(self, task_id: int):
        task_info = self.api.get(f"tasks/{task_id}")
        return task_info

    def get_lessons_task(self, lessons_ids: list):
        lessons_task = self.api.get(f"tasks", params={"lessons": lessons_ids})
        return lessons_task

    def get_lesson_task(self, lesson_id: int):
        lesson_task = self.api.get(f"lessons/{lesson_id}/tasks")
        return lesson_task

    def get_person_tasks(
        self,
        person_id: int,
        subject_id: int,
        start_time: datetime.datetime = datetime.datetime.now(),
        end_time: datetime.datetime = datetime.datetime.now(),
    ):
        person_subject_tasks = self.api.get(
            f"persons/{person_id}/tasks",
            params={"subject": subject_id, "from": start_time, "to": end_time},
        )
        return person_subject_tasks

    def get_teacher_students(self, teacher_id: int):
        teacher_students = self.api.get(f"teacher/{teacher_id}/students")
        return teacher_students

    def get_school_teachers(self, school_id: int):
        school_teachers = self.api.get(f"schools/{school_id}/teachers")
        return school_teachers

    def get_school_timetable(self, school_id: int):
        school_timetable = self.api.get(f"schools/{school_id}/timetables")
        return school_timetable

    def get_group_timetable(self, group_id: int):
        group_timetable = self.api.get(f"edu-groups/{group_id}/timetables")
        return group_timetable

    def get_feed(self):
        my_feed = self.api.get(
            f"users/me/feed", params={"date": datetime.datetime.now()}
        )
        return my_feed

    def get_user_groups(self, user_id: int):
        user_groups = self.api.get(f"users/{user_id}/groups")
        return user_groups

    def get_person_children(self, person_id: int):
        person_children = self.api.get(f"user/{person_id}/children")
        return person_children

    def get_user_children(self, user_id: int):
        children = self.api.get(f"user/{user_id}/children")
        return children

    def get_children(self):
        my_children = self.api.get(f"users/me/children")
        return my_children

    def get_user_relatives(self, user_id: int):
        user_rel = self.api.get(f"users/{user_id}/relatives")
        return user_rel

    def get_relatives(self):
        my_rel = self.api.get(f"users/me/relatives")
        return my_rel

    def get_children_relatives(self):
        my_children_relatives = self.api.get(f"users/me/childrenrelatives")
        return my_children_relatives

    def get_user_info(self, user_id: int):
        user_info = self.api.get(f"users/{user_id}")
        return user_info

    def get_roles(self):
        my_roles = self.api.get(f"users/me/roles")
        return my_roles

    def get_user_roles(self, user_id: int):
        user_roles = self.api.get(f"users/{user_id}/roles")
        return user_roles

    def get_group_average_marks(
        self,
        group_id: int,
        start_time=datetime.datetime.now(),
        end_time=datetime.datetime.now(),
    ):
        weighted_group_average_marks = self.api.get(
            f"edu-groups/{group_id}/wa-marks/{start_time}/{end_time}"
        )
        return weighted_group_average_marks

    def get_lesson_works(self, lesson_id: int):
        lesson_works = self.api.get(f"works", params={"lesson": lesson_id})
        return lesson_works

    def create_lesson_work(self, work: str):
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
        lesson_works = self.api.post(f"works", data={"work": work})
        return lesson_works

    def get_work_types(self, school_id: int):
        work_types = self.api.get(f"work-types/{school_id}")
        return work_types

    def invite_to_event(self, invite_id: int):
        response = self.api.post(f"events/{invite_id}/invite ")
        return response
