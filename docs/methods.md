## Документация

**Официальная документация на сайте** - [api.dnevnik.ru](https://api.dnevnik.ru/partners/swagger/ui/index#/)

## Методы dnevnik.ru:

### Authorities

- **get_organizations** - Список идентификаторов организаций текущего пользователя
```python
dn.get_organizations()
```

- **get_organization_info** - Данные указанной организации пользователя
```python
dn.get_organization_info()
```

### AverageMarks

- **get_person_average_marks** - Оценки персоны за отчетный период
```python
dn.get_person_average_marks(person_id=1000002385955, period=1000002385971)
```
|Параметр|Описание|
|-|-|
|person_id|ID выбранной персоны|
|period|Период для получения оценок в unixtime|

- **get_person_average_marks_by_subject** - Оценка персоны по предмету за отчетный период
```python
dn.get_person_average_marks_by_subjects(person_id=1000002385955, period=1000002385971, subject_id=683725334)
```
|Параметр|Описание|
|-|-|
|person_id|ID выбранной персоны|
|period|Период для получения оценок в unixtime|
|subject_id|ID выбранного предмета|

- **get_group_average_marks_by_date** - Оценки учебной группы по предмету за отчетный период до определенной даты
```python
import datetime

dn.get_group_average_marks_by_date(group_id=14455222, period=1000002385971, date=datetime.datetime(2019, 11, 8))
```
|Параметр|Описание|
|-|-|
|group_id|ID выбранной учебной группы|
|period|Период для получения оценок в unixtime|
|date|Конечная дата|

- **get_group_average_marks_by_time** - Оценки учебной группы за период
```python
import datetime

dn.get_group_average_marks_by_time(group_id=14455222, start_time=datetime.datetime(2019, 11, 5),
                                   end_time=datetime.datetime(2019, 11, 8))
```
|Параметр|Описание|
|-|-|
|group_id|ID выбранной учебной группы|
|start_time|Начальное время для получения оценок в unixtime|
|end_time|Конечное время для получения оценок в unixtime|

### Children

- **get_user_children** - Получение списка детей по идентификатору родительского пользователя
```python
dn.get_user_children(user_id=1000001509233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

- **get_person_children** - Получение списка детей по идентификатору родительской персоны
```python
dn.get_person_children(person_id=1000002385971)
```
|Параметр|Описание|
|-|-|
|person_id|ID выбранной персоны|

### Classmates

- **get_classmates** - Список id пользователей одноклассников текущего пользователя,
 если он является учеником, либо список активных участников образовательных групп пользователя во всех остальных случаях
```python
dn.get_classmates()
```

### Context

- **get_context** - Получение контекстной информации по пользователю
```python
dn.get_context()
```

- **get_user_context** - Получение контекстной информации по пользователю
```python
dn.get_user_context(user_id=1000001509233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

### CriteriaJournalMarks

- **get_final_group_marks_by_subjec**t - Метод, позволяющий получить итоговые оценки всего класса по указанному предмету
```python
dn.get_final_group_marks_by_subject(group_id=10033, subject_id=45666212)
```
|Параметр|Описание|
|-|-|
|group_id|ID выбранной группы|
|subject_id|ID выбранного предмета|

- **get_final_group_marks** - Метод, позволяющий получить итоговые оценки всего класса (каждого ученика) по всем предметам
```python
dn.get_final_group_marks(group_id=10033)
```
|Параметр|Описание|
|-|-|
|group_id|ID выбранной группы|

### EducationMemberships

- **get_user_memberships** - Список участий в школах для произвольного пользователя
```python
dn.get_user_memberships(user_id=1000001509233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

- **get_user_education** - Список участий в школах для произвольной персоны
```python
dn.get_user_education(person_id=1000001433233)
```
|Параметр|Описание|
|-|-|
|person_id|ID выбранной персоны|

- **get_schools** - Список идентификаторов школ текущего пользователя
```python
dn.get_schools()
```

- **get_user_schools** - Список идентификаторов школ произвольного пользователя
```python
dn.get_user_schools(user_id=1000005000233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

- **get_edu_groups** - Список идентификаторов классов текущего пользователя
```python
dn.get_edu_groups(user_id=1000005000233)
```

- **get_user_edu_groups** - Список идентификаторов классов произвольного пользователя
```python
dn.get_user_schools(user_id=1000005000233)
```
|Параметр|Описание|
|-|-|
|user_id|ID выбранного пользователя|

- **get_memberships** - Список участий в школах для текущего пользователя
```python
dn.get_memberships()
```

### EduGroups

>docs WIP now