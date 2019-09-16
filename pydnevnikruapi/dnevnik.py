import requests
import datetime


class DiaryBase:
    def __init__(self, login: str, password: str):
        self.session = requests.Session()
        self.host = 'https://api.dnevnik.ru/v2/'
        self.token = self.get_token(login, password)

    @staticmethod
    def get_token(login, password):
        token = requests.post('https://api.dnevnik.ru/v2/authorizations/bycredentials',
                              json={"client_id": "1d7bd105-4cd1-4f6c-9ecc-394e400b53bd",
                                    "client_secret": "5dcb5237-b5d3-406b-8fee-4441c3a66c99",
                                    "username": login, f"password": password,
                                    "scope": "Schools,Relatives,EduGroups,Lessons,marks,EduWorks,Avatar,"
                                             "EducationalInfo,CommonInfo,ContactInfo,FriendsAndRelatives,"
                                             "Files,Wall,Messages"}).json()['accessToken']

        return token

    def get(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}
        request = self.session.get(self.host + method, params=params,
                                   headers={'Access-Token': self.token}, **kwargs)
        return request

    def post(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}
        request = self.session.post(self.host + method, data=params,
                                    headers={'Access-Token': self.token}, **kwargs)
        return request

    def delete(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}
        request = self.session.delete(self.host + method, params=params,
                                      headers={'Access-Token': self.token}, **kwargs)
        return request

    def put(self, method: str, params=None, **kwargs):
        if params is None:
            params = {}
        request = self.session.put(self.host + method, data=params,
                                   headers={'Access-Token': self.token}, **kwargs)
        return request


class DiaryAPI:
    def __init__(self, login: str, password: str):
        self.api = DiaryBase(login, password)

    def get_my_school(self):
        school_id = self.api.get('schools/person-schools').json()
        return school_id

    def get_my_person(self):
        user_id = self.api.get('users/me').json()
        return user_id

    def get_my_classmates(self):
        classmates = self.api.get(f'users/me/classmates').json()
        return classmates

    def get_my_context(self):
        context = self.api.get(f'users/me/context').json()
        return context

    def get_user_context(self, user_id: int):
        #  TODO: check strange response
        context = self.api.get(f'users/{user_id}/context').json()
        return context

    def get_user_education_memberships(self, user_id: int):
        memberships = self.api.get(f'users/{user_id}/school-memberships').json()
        return memberships

    def get_user_education(self, user_id: int):
        education = self.api.get(f'users/{user_id}/education').json()
        return education

    def get_person_education_memberships(self, person_id: int):
        memberships = self.api.get(f'persons/{person_id}/school-memberships').json()
        return memberships

    def get_my_schools(self):
        schools = self.api.get(f'users/me/schools').json()
        return schools

    def get_user_schools(self, user_id: int):
        schools = self.api.get(f'users/{user_id}/schools').json()
        return schools

    def get_my_edu_groups(self):
        edu_groups = self.api.get(f'users/me/edu-groups').json()
        return edu_groups

    def get_user_edu_groups(self, user_id: int):
        edu_groups = self.api.get(f'users/{user_id}/edu-groups').json()
        return edu_groups

    def get_my_schools_memberships(self):
        schools_memberships = self.api.get(f'users/me/school-memberships').json()
        return schools_memberships

    def get_edu_group_info(self, edu_group_id: int):
        edu_group_info = self.api.get(f'edu-groups/{edu_group_id}').json()
        return edu_group_info

    def get_edu_groups_info(self, edu_groups_list: list):
        edu_groups_info = self.api.get(f'edu-groups', params={'eduGroups': edu_groups_list}).json()
        return edu_groups_info

    def get_school_edu_groups(self, school_id: int):
        school_edu_groups = self.api.get(f'schools/{school_id}/edu-groups').json()
        return school_edu_groups

    def get_person_edu_groups(self, person_id: int):
        person_edu_groups = self.api.get(f'persons/{person_id}/edu-groups').json()
        return person_edu_groups

    def get_person_edu_groups_all(self, person_id: int):
        person_edu_all = self.api.get(f'persons/{person_id}/edu-groups/all').json()
        return person_edu_all

    def get_person_edu_groups_in_school(self, person_id: int, school_id: int):
        person_edu_groups_in_school = self.api.get(f'persons/{person_id}/schools/{school_id}/edu-groups').json()
        return person_edu_groups_in_school

    def get_edu_groups_pupils_list(self, edu_group_id: int):
        edu_groups_list = self.api.get(f'edu-groups/{edu_group_id}/persons').json()
        return edu_groups_list

    def get_edu_groups_parallel(self, group_id: int):
        edu_groups_list = self.api.get(f'edu-groups/{group_id}/parallel').json()
        return edu_groups_list

    def get_edu_group_marks(self, group_id: int):
        edu_groups_marks = self.api.get(f'edu-groups/{group_id}/final-marks').json()
        return edu_groups_marks

    def get_person_marks_in_group(self, person_id: int, group_id: int):
        #  TODO: check strange response
        person_marks_in_group = self.api.get(f'persons/{person_id}/edu-groups/{group_id}/final-marks').json()
        return person_marks_in_group

    def get_final_person_marks_in_group(self, person_id: int, group_id: int):
        person_final_marks_in_group = self.api.get(f'persons/{person_id}/edu-groups/{group_id}/allfinalmarks').json()
        return person_final_marks_in_group

    def get_group_subject_final_marks(self, group_id: int, subject_id: int):
        group_subject_marks = self.api.get(f'edu-groups/{group_id}/subjects/{subject_id}/final-marks').json()
        return group_subject_marks

    def get_my_friends(self):
        my_friends = self.api.get(f'users/me/friends').json()
        return my_friends

    def get_user_friends(self, user_id: int):
        user_friends = self.api.get(f'users/{user_id}/friends').json()
        return user_friends

    def get_my_school_homework(self, school_id: int, start_time=datetime.datetime.now(),
                               end_time=datetime.datetime.now()):
        homework = self.api.get(f'users/me/school/{school_id}/homeworks',
                                params={'startDate': start_time, 'endDate': end_time}).json()
        return homework

    def get_my_homework_by_id(self, homework_id: int):
        homework = self.api.get(f'users/me/school/homeworks', params={'homeworkId': homework_id}).json()
        return homework

    def get_person_school_homework(self, school_id: int, person_id: int, start_time=datetime.datetime.now(),
                                   end_time=datetime.datetime.now()):
        homework = self.api.get(f'persons/{person_id}/school/{school_id}/homeworks',
                                params={'startDate': start_time, 'endDate': end_time}).json()
        return homework

    def delete_lesson_log(self, lesson_id: int, person_id: int):
        response = self.api.delete(f'lessons/{lesson_id}/log-entries', params={'person': person_id}).json()
        return response

    def get_lesson_log(self, lesson_id: int):
        lesson_log = self.api.get(f'lessons/{lesson_id}/log-entries').json()
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
        lesson_log = self.api.post(f'lessons/{lesson_id}/log-entries', data={'lessonLogEntry': lesson_log_entry}).json()
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
        lesson_log = self.api.put(f'lessons/{lesson_id}/log-entries',
                                  data={'person': person_id, 'lessonLogEntry': lesson_log_entry}).json()
        return lesson_log

    def get_lesson_logs(self, lessons_ids: list):
        lesson_logs = self.api.get(f'lesson-log-entries', params={'lessons': lessons_ids}).json()
        return lesson_logs

    def get_person_lesson_log(self, person_id: int, lesson_id: int):
        lesson_logs = self.api.get(f'lesson-log-entries/lesson/{lesson_id}/person/{person_id}').json()
        return lesson_logs

    def get_group_lesson_log(self, group_id: int, subject_id: int, start_time=datetime.datetime.now(),
                             end_time=datetime.datetime.now()):
        lesson_logs = self.api.get(f'lesson-log-entries/group/{group_id}',
                                   params={'subject': subject_id, 'from': start_time, 'to': end_time}).json()
        return lesson_logs

    def get_person_subject_lesson_log(self, person_id: int, subject_id: int, start_time=datetime.datetime.now(),
                                      end_time=datetime.datetime.now()):
        lesson_logs = self.api.get(
            f'lesson-log-entries/person/{person_id}/subject/{subject_id}',
            params={'subject': subject_id, 'from': start_time, 'to': end_time}).json()
        return lesson_logs

    def get_person_lesson_logs(self, person_id: int, start_time=datetime.datetime.now(), end_time=datetime.datetime.now()):
        lesson_logs = self.api.get(
            f'persons/{person_id}/lesson-log-entries', params={'startDate': start_time, 'endDate': end_time}).json()
        return lesson_logs

    def get_lesson_log_statuses(self):
        lesson_logs_statuses = self.api.get(f'lesson-log-entries/statuses').json()
        return lesson_logs_statuses

    def get_lesson_info(self, lesson_id: int):
        lesson_info = self.api.get(f'lessons/{lesson_id}').json()
        return lesson_info

    def get_many_lessons_info(self, lessons_list: list):
        lesson_info = self.api.post(f'lessons/many', data={'lessons': lessons_list}).json()
        return lesson_info

    def get_group_lessons_info(self, group_id: int, start_time=datetime.datetime.now(), end_time=datetime.datetime.now()):
        lessons_info = self.api.get(f'edu-groups/{group_id}/lessons/{start_time}/{end_time}').json()
        return lessons_info

    def get_group_lessons_subject_info(self, group_id: int, start_time=datetime.datetime.now(),
                                       end_time=datetime.datetime.now()):
        lessons_info = self.api.get(f'edu-groups/{group_id}/lessons/{start_time}/{end_time}').json()
        return lessons_info

    def get_marks_histogram(self, work_id: int):
        marks_histogram = self.api.get(f'works/{work_id}/marks/histogram').json()
        return marks_histogram

    def get_subject_marks_histogram_by_period(self, group_id: int, period_id: int, subject_id: int):
        marks_histogram = self.api.get(
            f'periods/{period_id}/subjects/{subject_id}/groups/{group_id}/marks/histogram').json()
        return marks_histogram

    def get_mark_by_mark_id(self, mark_id: int):
        mark_info = self.api.get(f'marks/{mark_id}').json()
        return mark_info

    def get_marks_by_work_id(self, work_id: int):
        marks = self.api.get(f'works/{work_id}/marks').json()
        return marks

    def get_marks_by_lesson_id(self, lesson_id: int):
        marks = self.api.get(f'lessons/{lesson_id}/marks').json()
        return marks

    def get_marks_by_lessons_ids(self, lessons_ids: list):
        marks = self.api.post(f'lessons/marks', data={'lessons': lessons_ids}).json()
        return marks

    def get_group_marks(self, group_id: int, start_time=datetime.datetime.now(), end_time=datetime.datetime.now()):
        marks = self.api.get(f'edu-groups/{group_id}/marks/{start_time}/{end_time}').json()
        return marks

    def get_group_subject_marks(self, group_id: int, subject_id: int, start_time=datetime.datetime.now(),
                                end_time=datetime.datetime.now()):
        marks = self.api.get(
            f'edu-groups/{group_id}/subjects/{subject_id}/marks/{start_time}/{end_time}').json()
        return marks

    def get_person_school_marks(self, person_id: int, school_id: int, start_time=datetime.datetime.now(),
                                end_time=datetime.datetime.now()):
        marks = self.api.get(f'persons/{person_id}/schools/{school_id}/marks/{start_time}/{end_time}').json()
        return marks

    def get_person_lessons_marks(self, person_id: int, lesson_id: int):
        marks = self.api.get(f'persons/{person_id}/lessons/{lesson_id}/marks').json()
        return marks

    def get_person_work_marks(self, person_id: int, work_id: int):
        marks = self.api.get(f'persons/{person_id}/works/{work_id}/marks').json()
        return marks

    def get_person_subject_marks(self, person_id: int, subject_id: int, start_time=datetime.datetime.now(),
                                 end_time=datetime.datetime.now()):
        marks = self.api.get(f'persons/{person_id}/subjects/{subject_id}/marks/{start_time}/{end_time}', ).json()
        return marks

    def get_marks_by_date(self, person_id: int, date=datetime.datetime.now()):
        marks = self.api.get(f'persons/{person_id}/marks/{date}').json()
        return marks

    def get_marks_values(self):
        marks_values = self.api.get(f'https://api.dnevnik.ru/v2.0/marks/values').json()
        return marks_values

    def get_marks_values_by_type(self, marks_type: str):
        marks_values = self.api.get(f'marks/values/type/{marks_type}').json()
        return marks_values

    def get_persons_in_group(self, group_id: int):
        persons = self.api.get(f'persons', params={"eduGroup": group_id}).json()
        return persons

    def get_person_info(self, person_id: int):
        person_info = self.api.get(f'persons/{person_id}').json()
        return person_info

    def get_recent_person_marks(self, person_id: int, group_id: int):
        recent_person_marks = self.api.get(f'persons/{person_id}/group/{group_id}/recentmarks').json()
        return recent_person_marks

    def get_group_reports(self, group_id: int):
        group_reports = self.api.get(f'edu-groups/{group_id}/reporting-periods').json()
        return group_reports

    def get_person_schedule(self, person_id, group_id, start_time=datetime.datetime.now(),
                            end_time=datetime.datetime.now()):
        person_schedule = self.api.get(f'https://api.dnevnik.ru/v2.0/persons/{person_id}/groups/{group_id}/schedules',
                                       params={'startDate': start_time, 'endDate': end_time}).json()
        return person_schedule

    def get_best_schools(self, start_time=datetime.datetime.now(), end_time=datetime.datetime.now()):
        best_schools = self.api.get(f'school-rating/from/{start_time}/to/{end_time}').json()
        return best_schools

    def get_school_profile(self, school_id: int):
        school_profile = self.api.get(f'schools/{school_id}').json()
        return school_profile

    def get_schools_profiles(self, schools_ids: list):
        school_profiles = self.api.get(f'schools', params={'schools': schools_ids}).json()
        return school_profiles

    def get_my_person_schools(self):
        person_schools = self.api.get(f'schools/person-schools').json()
        return person_schools

    def get_all_schools(self):
        all_schools = self.api.get(f'schools/cities').json()
        return all_schools

    def get_school_params(self, school_id: int):
        school_params = self.api.get(f'schools/{school_id}/parameters', ).json()
        return school_params

    def get_group_subjects(self, group_id: int):
        group_subjects = self.api.get(f'edu-groups/{group_id}/subjects').json()
        return group_subjects

    def get_school_subjects(self, school_id: int):
        school_subjects = self.api.get(f'schools/{school_id}/subjects').json()
        return school_subjects

    def get_task_info(self, task_id: int):
        task_info = self.api.get(f'tasks/{task_id}').json()
        return task_info

    def get_lessons_task(self, lessons_ids: list):
        lessons_task = self.api.get(f'tasks', params={'lessons': lessons_ids}).json()
        return lessons_task

    def get_lesson_task(self, lesson_id: int):
        lesson_task = self.api.get(f'lessons/{lesson_id}/tasks').json()
        return lesson_task

    def get_person_subject_tasks(self, person_id: int, subject_id: int, start_time=datetime.datetime.now(),
                                 end_time=datetime.datetime.now()):
        person_subject_tasks = self.api.get(f'persons/{person_id}/tasks',
                                            params={'subject': subject_id, 'from': start_time, 'to': end_time}).json()
        return person_subject_tasks

    def get_teacher_students(self, teacher_id: int):
        teacher_students = self.api.get(f'teacher/{teacher_id}/students').json()
        return teacher_students

    def get_school_teachers(self, school_id: int):
        school_teachers = self.api.get(f'schools/{school_id}/teachers').json()
        return school_teachers

    def get_school_timetable(self, school_id: int):
        school_timetable = self.api.get(f'schools/{school_id}/timetables').json()
        return school_timetable

    def get_group_timetable(self, group_id: int):
        group_timetable = self.api.get(f'edu-groups/{group_id}/timetables').json()
        return group_timetable

    def get_my_feed(self):
        my_feed = self.api.get(f'users/me/feed', params={'date': datetime.datetime.now()}).json()
        return my_feed

    def get_user_groups(self, user_id: int):
        user_groups = self.api.get(f'users/{user_id}/groups').json()
        return user_groups

    def get_my_children(self):
        my_children = self.api.get(f'users/me/children').json()
        return my_children

    def get_user_relatives(self, user_id: int):
        user_rel = self.api.get(f'users/{user_id}/relatives').json()
        return user_rel

    def get_my_relatives(self):
        my_rel = self.api.get(f'users/me/relatives').json()
        return my_rel

    def get_my_children_relatives(self):
        my_children_relatives = self.api.get(f'users/me/childrenrelatives').json()
        return my_children_relatives

    def get_user_info(self, user_id: int):
        user_info = self.api.get(f'users/{user_id}').json()
        return user_info

    def get_my_roles(self):
        my_roles = self.api.get(f'users/me/roles').json()
        return my_roles

    def get_user_roles(self, user_id: int):
        user_roles = self.api.get(f'users/{user_id}/roles').json()
        return user_roles

    def get_weighted_group_average_marks(self, group_id: int, start_time=datetime.datetime.now(),
                                         end_time=datetime.datetime.now()):
        weighted_group_average_marks = self.api.get(f'edu-groups/{group_id}/wa-marks/{start_time}/{end_time}').json()
        return weighted_group_average_marks

    def get_lesson_works(self, lesson_id: int):
        lesson_works = self.api.get(f'works', params={'lesson': lesson_id}).json()
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
        lesson_works = self.api.post(f'works', data={'work': work}).json()
        return lesson_works

    def get_work_types(self, school_id: int):
        work_types = self.api.get(f'work-types/{school_id}', ).json()
        return work_types
