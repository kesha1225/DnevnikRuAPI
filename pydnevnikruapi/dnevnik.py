import requests
import datetime


class DiaryAPI:

    def __init__(self, login, password):
        self.token = self.get_token(login, password)

    @staticmethod
    def get_token(login, password):
        token = requests.post('https://api.dnevnik.ru/v1/authorizations/bycredentials',
                              json={"client_id": "1d7bd105-4cd1-4f6c-9ecc-394e400b53bd",
                                    "client_secret": "5dcb5237-b5d3-406b-8fee-4441c3a66c99",
                                    "username": f"{login}", f"password": f"{password}",
                                    "scope": "Schools,Relatives,EduGroups,Lessons,marks,EduWorks,Avatar,"
                                             "EducationalInfo,CommonInfo,ContactInfo,FriendsAndRelatives,"
                                             "Files,Wall,Messages"}).json()['accessToken']

        return token

    def get_school_id(self):
        school_id = requests.get('https://api.dnevnik.ru/v2.0/schools/person-schools',
                                 headers={'Access-Token': self.token}).json()[0]['id']

        return school_id

    def get_my_person_id(self):
        user_id = requests.get('https://api.dnevnik.ru/v2.0/users/me',
                               headers={'Access-Token': self.token}).json()
        return user_id['personId']

    def get_my_classmates(self):
        classmates = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/classmates',
                                  headers={'Access-Token': self.token}).json()
        return classmates

    def get_my_context(self):
        context = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/context',
                               headers={'Access-Token': self.token}).json()
        return context

    def get_user_context(self, user_id):
        #  TODO: check strange response
        context = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}/context',
                               headers={'Access-Token': self.token}).json()
        return context

    def get_user_education_memberships(self, user_id):
        memberships = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}/school-memberships',
                                   headers={'Access-Token': self.token}).json()
        return memberships

    def get_user_education(self, user_id):
        education = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}/education',
                                 headers={'Access-Token': self.token}).json()
        return education

    def get_person_education_memberships(self, person_id):
        memberships = requests.get(f'https://api.dnevnik.ru/v2.0/persons/{person_id}/school-memberships',
                                   headers={'Access-Token': self.token}).json()
        return memberships

    def get_my_schools(self):
        schools = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/schools',
                               headers={'Access-Token': self.token}).json()
        return schools

    def get_user_schools(self, user_id):
        schools = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}/schools',
                               headers={'Access-Token': self.token}).json()
        return schools

    def get_my_edu_groups(self):
        edu_groups = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/edu-groups',
                                  headers={'Access-Token': self.token}).json()
        return edu_groups

    def get_user_edu_groups(self, user_id):
        edu_groups = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}/edu-groups',
                                  headers={'Access-Token': self.token}).json()
        return edu_groups

    def get_my_schools_memberships(self):
        schools_memberships = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/school-memberships',
                                           headers={'Access-Token': self.token}).json()
        return schools_memberships

    def get_edu_group_info(self, edu_group_id):
        edu_group_info = requests.get(f'https://api.dnevnik.ru/v2.0/edu-groups/{edu_group_id}',
                                      headers={'Access-Token': self.token}).json()
        return edu_group_info

    def get_edu_groups_info(self, edu_groups_list: list):
        edu_groups_info = requests.get(f'https://api.dnevnik.ru/v2.0/edu-groups',
                                       headers={'Access-Token': self.token},
                                       params={'eduGroups': edu_groups_list}).json()
        return edu_groups_info

    def get_school_edu_groups(self, school_id):
        school_edu_groups = requests.get(f'https://api.dnevnik.ru/v2.0/schools/{school_id}/edu-groups',
                                         headers={'Access-Token': self.token}).json()
        return school_edu_groups

    def get_person_edu_groups(self, person_id):
        person_edu_groups = requests.get(f'https://api.dnevnik.ru/v2.0/persons/{person_id}/edu-groups',
                                         headers={'Access-Token': self.token}).json()
        return person_edu_groups

    def get_person_edu_groups_all(self, person_id):  # Прямо с первого класса все ваши образовательные группы
        person_edu_all = requests.get(f'https://api.dnevnik.ru/v2.0/persons/{person_id}/edu-groups/all',
                                      headers={'Access-Token': self.token}).json()
        return person_edu_all

    def get_person_edu_groups_in_school(self, person_id, school_id):
        person_edu_groups_in_school = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/schools/{school_id}/edu-groups',
            headers={'Access-Token': self.token}).json()
        return person_edu_groups_in_school

    def get_edu_groups_pupils_list(self, edu_group_id):  # участники какой-либо обр. группы
        edu_groups_list = requests.get(f'https://api.dnevnik.ru/v2.0/edu-groups/{edu_group_id}/persons',
                                       headers={'Access-Token': self.token}).json()
        return edu_groups_list

    def get_edu_groups_parallel(self, group_id):
        edu_groups_list = requests.get(f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/parallel',
                                       headers={'Access-Token': self.token}).json()
        return edu_groups_list

    def get_edu_group_marks(self, group_id):
        edu_groups_marks = requests.get(f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/final-marks',
                                        headers={'Access-Token': self.token}).json()
        return edu_groups_marks

    def get_person_marks_in_group(self, person_id, group_id):
        #  TODO: check strange response
        person_marks_in_group = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/edu-groups/{group_id}/final-marks',
            headers={'Access-Token': self.token}).json()
        return person_marks_in_group

    def get_final_person_marks_in_group(self, person_id, group_id):
        person_final_marks_in_group = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/edu-groups/{group_id}/allfinalmarks',
            headers={'Access-Token': self.token}).json()
        return person_final_marks_in_group

    def get_group_subject_final_marks(self, group_id, subject_id):
        group_subject_marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/subjects/{subject_id}/final-marks',
            headers={'Access-Token': self.token}).json()
        return group_subject_marks

    def get_my_friends(self):
        my_friends = requests.get(
            f'https://api.dnevnik.ru/v2.0/users/me/friends', headers={'Access-Token': self.token}).json()
        return my_friends

    def get_user_friends(self, user_id):
        user_friends = requests.get(
            f'https://api.dnevnik.ru/v2.0/users/{user_id}/friends', headers={'Access-Token': self.token}).json()
        return user_friends

    def get_my_school_homework(self, school_id, start_time, end_time):
        homework = requests.get(
            f'https://api.dnevnik.ru/v2.0/users/me/school/{school_id}/homeworks',
            headers={'Access-Token': self.token}, params={'startDate': start_time, 'endDate': end_time}).json()
        return homework

    def get_my_homework_by_id(self, homework_id):
        homework = requests.get(
            f'https://api.dnevnik.ru/v2.0/users/me/school/homeworks',
            headers={'Access-Token': self.token}, params={'homeworkId': homework_id}).json()
        return homework

    def get_person_school_homework(self, school_id, person_id, start_time, end_time):
        homework = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/school/{school_id}/homeworks',
            headers={'Access-Token': self.token}, params={'startDate': start_time, 'endDate': end_time}).json()
        return homework

    def delete_lesson_log(self, lesson_id, person_id):
        response = requests.delete(
            f'https://api.dnevnik.ru/v2.0/lessons/{lesson_id}/log-entries',
            headers={'Access-Token': self.token}, params={'person': person_id}).json()
        return response

    def get_lesson_log(self, lesson_id):
        lesson_log = requests.get(
            f'https://api.dnevnik.ru/v2.0/lessons/{lesson_id}/log-entries', headers={'Access-Token': self.token}).json()
        return lesson_log

    def post_lesson_log(self, lesson_id, lesson_log_entry):
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
        lesson_log = requests.post(
            f'https://api.dnevnik.ru/v2.0/lessons/{lesson_id}/log-entries',
            headers={'Access-Token': self.token}, data={'lessonLogEntry': lesson_log_entry}).json()
        return lesson_log

    def put_lesson_log(self, lesson_id, person_id, lesson_log_entry):
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
        lesson_log = requests.put(
            f'https://api.dnevnik.ru/v2.0/lessons/{lesson_id}/log-entries',
            headers={'Access-Token': self.token}, data={'person': person_id, 'lessonLogEntry': lesson_log_entry}).json()
        return lesson_log

    def get_lesson_logs(self, lessons_ids: list):
        lesson_logs = requests.get(
            f'https://api.dnevnik.ru/v2.0/lesson-log-entries',
            headers={'Access-Token': self.token}, params={'lessons': lessons_ids}).json()
        return lesson_logs

    def get_person_lesson_log(self, person_id, lesson_id):
        lesson_logs = requests.get(
            f'https://api.dnevnik.ru/v2.0/lesson-log-entries/lesson/{lesson_id}/person/{person_id}',
            headers={'Access-Token': self.token}).json()
        return lesson_logs

    def get_group_lesson_log(self, group_id, subject_id, start_time, end_time):
        lesson_logs = requests.get(
            f'https://api.dnevnik.ru/v2.0/lesson-log-entries/group/{group_id}',
            headers={'Access-Token': self.token}, params={'subject': subject_id,
                                                          'from': start_time, 'to': end_time}).json()
        return lesson_logs

    def get_person_subject_lesson_log(self, person_id, subject_id, start_time, end_time):
        lesson_logs = requests.get(
            f'https://api.dnevnik.ru/v2.0/lesson-log-entries/person/{person_id}/subject/{subject_id}',
            headers={'Access-Token': self.token}, params={'subject': subject_id,
                                                          'from': start_time, 'to': end_time}).json()
        return lesson_logs

    def get_person_lesson_logs(self, person_id, start_time, end_time):
        lesson_logs = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/lesson-log-entries',
            headers={'Access-Token': self.token}, params={'startDate': start_time, 'endDate': end_time}).json()
        return lesson_logs

    def get_lesson_log_statuses(self):
        lesson_logs_statuses = requests.get(
            f'https://api.dnevnik.ru/v2.0/lesson-log-entries/statuses', headers={'Access-Token': self.token}).json()
        return lesson_logs_statuses

    def get_lesson_info(self, lesson_id):
        lesson_info = requests.get(
            f'https://api.dnevnik.ru/v2.0/lessons/{lesson_id}', headers={'Access-Token': self.token}).json()
        return lesson_info

    def get_many_lessons_info(self, lessons_list: list):
        lesson_info = requests.post(
            f'https://api.dnevnik.ru/v2.0/lessons/many', headers={'Access-Token': self.token},
            data={'lessons': lessons_list}).json()
        return lesson_info

    def get_group_lessons_info(self, group_id, start_time, end_time):
        lessons_info = requests.get(
            f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/lessons/{start_time}/{end_time}',
            headers={'Access-Token': self.token}).json()
        return lessons_info

    def get_group_lessons_subject_info(self, group_id, start_time, end_time):
        lessons_info = requests.get(
            f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/lessons/{start_time}/{end_time}',
            headers={'Access-Token': self.token}).json()
        return lessons_info

    def get_marks_histogram(self, work_id):
        marks_histogram = requests.get(
            f'https://api.dnevnik.ru/v2.0/works/{work_id}/marks/histogram', headers={'Access-Token': self.token}).json()
        return marks_histogram

    def get_subject_marks_histogram_by_period(self, group_id, period_id, subject_id):
        marks_histogram = requests.get(
            f'https://api.dnevnik.ru/v2.0/periods/{period_id}/subjects/{subject_id}/groups/{group_id}/marks/histogram',
            headers={'Access-Token': self.token}).json()
        return marks_histogram

    def get_mark_by_mark_id(self, mark_id):
        mark_info = requests.get(
            f'https://api.dnevnik.ru/v2.0/marks/{mark_id}', headers={'Access-Token': self.token}).json()
        return mark_info

    def get_marks_by_work_id(self, work_id):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/works/{work_id}/marks', headers={'Access-Token': self.token}).json()
        return marks

    def get_marks_by_lesson_id(self, lesson_id):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/lessons/{lesson_id}/marks', headers={'Access-Token': self.token}).json()
        return marks

    def get_marks_by_lessons_ids(self, lessons_ids: list):
        marks = requests.post(
            f'https://api.dnevnik.ru/v2.0/lessons/marks', headers={'Access-Token': self.token},
            data={'lessons': lessons_ids}).json()
        return marks

    def get_group_marks(self, group_id, start_time, end_time):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/marks/{start_time}/{end_time}',
            headers={'Access-Token': self.token}).json()
        return marks

    def get_group_subject_marks(self, group_id, subject_id, start_time, end_time):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/subjects/{subject_id}/marks/{start_time}/{end_time}',
            headers={'Access-Token': self.token}).json()
        return marks

    def get_person_school_marks(self, person_id, school_id, start_time, end_time):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/schools/{school_id}/marks/{start_time}/{end_time}',
            headers={'Access-Token': self.token}).json()
        return marks

    def get_person_lessons_marks(self, person_id, lesson_id):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/lessons/{lesson_id}/marks',
            headers={'Access-Token': self.token}).json()
        return marks

    def get_person_work_marks(self, person_id, work_id):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/works/{work_id}/marks',
            headers={'Access-Token': self.token}).json()
        return marks

    def get_person_subject_marks(self, person_id, subject_id, start_time, end_time):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/subjects/{subject_id}/marks/{start_time}/{end_time}',
            headers={'Access-Token': self.token}).json()
        return marks

    def get_marks_by_date(self, person_id, date):
        marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/marks/{date}',
            headers={'Access-Token': self.token}).json()
        return marks

    def get_marks_values(self):
        marks_values = requests.get(
            f'https://api.dnevnik.ru/v2.0/marks/values', headers={'Access-Token': self.token}).json()
        return marks_values

    def get_marks_values_by_type(self, marks_type: str):
        marks_values = requests.get(
            f'https://api.dnevnik.ru/v2.0/marks/values/type/{marks_type}', headers={'Access-Token': self.token}).json()
        return marks_values

    def get_persons_in_group(self, group_id):
        persons = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons', params={"eduGroup": group_id},
            headers={'Access-Token': self.token}).json()
        return persons

    def get_person_info(self, person_id):
        person_info = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}', headers={'Access-Token': self.token}).json()
        return person_info

    def get_recent_person_marks(self, person_id, group_id):
        recent_person_marks = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/group/{group_id}/recentmarks',
            headers={'Access-Token': self.token}).json()
        return recent_person_marks

    def get_regions(self):
        regions = requests.get(
            f'https://api.dnevnik.ru/authorizations/esia/v2.0/regions', headers={'Access-Token': self.token}).json()
        return regions

    def get_group_reports(self, group_id):
        group_reports = requests.get(
            f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/reporting-periods',
            headers={'Access-Token': self.token}).json()
        return group_reports

    def get_person_schedule(self, person_id, group_id, start_time, end_time):
        person_schedule = requests.get(
            f'https://api.dnevnik.ru/v2.0/persons/{person_id}/groups/{group_id}/schedules',
            headers={'Access-Token': self.token}, params={'startDate': start_time, 'endDate': end_time}).json()
        return person_schedule

    def get_best_schools(self, start_time, end_time):
        best_schools = requests.get(
            f'https://api.dnevnik.ru/v2.0/school-rating/from/{start_time}/to/{end_time}',
            headers={'Access-Token': self.token}).json()
        return best_schools

    def get_school_profile(self, school_id):
        school_profile = requests.get(
            f'https://api.dnevnik.ru/v2.0/schools/{school_id}', headers={'Access-Token': self.token}).json()
        return school_profile

    def get_schools_profiles(self, schools_ids: list):
        school_profiles = requests.get(
            f'https://api.dnevnik.ru/v2.0/schools', params={'schools': schools_ids},
            headers={'Access-Token': self.token}).json()
        return school_profiles

    def get_my_person_schools(self):
        person_schools = requests.get(
            f'https://api.dnevnik.ru/v2.0/schools/person-schools', headers={'Access-Token': self.token}).json()
        return person_schools

    def get_all_schools(self):
        all_schools = requests.get(
            f'https://api.dnevnik.ru/v2.0/schools/cities', headers={'Access-Token': self.token}).json()
        return all_schools

    def get_school_params(self, school_id):
        school_params = requests.get(f'https://api.dnevnik.ru/v2.0/schools/{school_id}/parameters',
                                     headers={'Access-Token': self.token}).json()
        return school_params

    def get_group_subjects(self, group_id):
        group_subjects = requests.get(f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/subjects',
                                      headers={'Access-Token': self.token}).json()
        return group_subjects

    def get_school_subjects(self, school_id):
        school_subjects = requests.get(f'https://api.dnevnik.ru/v2.0/schools/{school_id}/subjects',
                                       headers={'Access-Token': self.token}).json()
        return school_subjects

    def get_task_info(self, task_id):
        task_info = requests.get(f'https://api.dnevnik.ru/v2.0/tasks/{task_id}',
                                 headers={'Access-Token': self.token}).json()
        return task_info

    def get_lessons_task(self, lessons_ids: list):
        lessons_task = requests.get(f'https://api.dnevnik.ru/v2.0/tasks', params={'lessons': lessons_ids},
                                    headers={'Access-Token': self.token}).json()
        return lessons_task

    def get_lesson_task(self, lesson_id):
        lesson_task = requests.get(f'https://api.dnevnik.ru/v2.0/lessons/{lesson_id}/tasks',
                                   headers={'Access-Token': self.token}).json()
        return lesson_task

    def get_person_subject_tasks(self, person_id, subject_id, start_time, end_time):
        person_subject_tasks = requests.get(f'https://api.dnevnik.ru/v2.0/persons/{person_id}/tasks',
                                            params={'subject': subject_id, 'from': start_time, 'to': end_time},
                                            headers={'Access-Token': self.token}).json()
        return person_subject_tasks

    def get_teacher_students(self, teacher_id):
        teacher_students = requests.get(f'https://api.dnevnik.ru/v2.0/teacher/{teacher_id}/students',
                                        headers={'Access-Token': self.token}).json()
        return teacher_students

    def get_school_teachers(self, school_id):
        school_teachers = requests.get(f'https://api.dnevnik.ru/v2.0/schools/{school_id}/teachers',
                                       headers={'Access-Token': self.token}).json()
        return school_teachers

    def get_school_timetable(self, school_id):
        school_timetable = requests.get(f'https://api.dnevnik.ru/v2.0/schools/{school_id}/timetables',
                                        headers={'Access-Token': self.token}).json()
        return school_timetable

    def get_group_timetable(self, group_id):
        group_timetable = requests.get(f'https://api.dnevnik.ru/v2.0/edu-groups/{group_id}/timetables',
                                       headers={'Access-Token': self.token}).json()
        return group_timetable

    def get_my_feed(self):
        my_feed = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/feed',
                               params={'date': datetime.datetime.now()},
                               headers={'Access-Token': self.token}).json()
        return my_feed

    def get_user_groups(self, user_id):
        user_groups = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}/groups',
                                   headers={'Access-Token': self.token}).json()
        return user_groups

    def get_my_children(self):
        my_children = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/children',
                                   headers={'Access-Token': self.token}).json()
        return my_children

    def get_user_relatives(self, user_id):
        user_rel = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}/relatives',
                                headers={'Access-Token': self.token}).json()
        return user_rel

    def get_my_relatives(self):
        my_rel = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/relatives',
                              headers={'Access-Token': self.token}).json()
        return my_rel

    def get_my_children_relatives(self):
        my_children_relatives = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/childrenrelatives',
                                             headers={'Access-Token': self.token}).json()
        return my_children_relatives

    def get_my_user_id(self):
        user_id = requests.get('https://api.dnevnik.ru/v2.0/users/me',
                               headers={'Access-Token': self.token}).json()
        return user_id['id']

    def get_user_info(self, user_id):
        user_info = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}',
                                 headers={'Access-Token': self.token}).json()
        return user_info

    def get_my_roles(self):
        my_roles = requests.get(f'https://api.dnevnik.ru/v2.0/users/me/roles',
                                headers={'Access-Token': self.token}).json()
        return my_roles

    def get_user_roles(self, user_id):
        user_roles = requests.get(f'https://api.dnevnik.ru/v2.0/users/{user_id}/roles',
                                  headers={'Access-Token': self.token}).json()
        return user_roles

    def get_weighted_group_average_marks(self, group_id, start_time, end_time):
        weighted_group_average_marks = requests.get(f'https://api.dnevnik.ru/v2.0/edu-groups/'
                                                    f'{group_id}/wa-marks/{start_time}/{end_time}',
                                                    headers={'Access-Token': self.token}).json()
        return weighted_group_average_marks

    def get_lesson_works(self, lesson_id):
        lesson_works = requests.get(f'https://api.dnevnik.ru/v2.0/works', params={'lesson': lesson_id},
                                    headers={'Access-Token': self.token}).json()
        return lesson_works

    def create_lesson_work(self, work):
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
        lesson_works = requests.post(f'https://api.dnevnik.ru/v2.0/works', data={'work': work},
                                     headers={'Access-Token': self.token}).json()
        return lesson_works

    def get_work_types(self, school_id):
        work_types = requests.get(f'https://api.dnevnik.ru/v2.0/work-types/{school_id}',
                                  headers={'Access-Token': self.token}).json()
        return work_types
