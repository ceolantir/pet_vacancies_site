from functools import partial
from abc import ABCMeta, abstractmethod


# базовая модель резюме
class BaseResume(metaclass=ABCMeta):
    STATUS_CHOICES = {
        'NS': 'Не ищу работу',
        'SS': 'Рассматриваю предложения',
        'IS': 'Ищу работу',
    }
    GRADE_CHOICES = {
        'TR': 'Стажер',
        'JR': 'Джуниор',
        'MD': 'Мидл',
        'SR': 'Синьор',
        'TM': 'Лид',
    }

    @abstractmethod
    def change_name(self, name):
        raise NotImplementedError()

    @abstractmethod
    def change_status(self, status):
        raise NotImplementedError()

    @abstractmethod
    def change_speciality(self, speciality):
        raise NotImplementedError()

    @abstractmethod
    def change_grade(self, grade):
        raise NotImplementedError()


# модель резюме
class Resume(BaseResume):
    def __init__(self, name, status_code, speciality, grade_code):
        self.name = name
        self.status = self.STATUS_CHOICES[status_code]
        self.speciality = speciality
        self.grade = self.GRADE_CHOICES[grade_code]

    def change_name(self, name):
        self.name = name

    def change_status(self, status):
        self.status = self.STATUS_CHOICES[status]

    def change_speciality(self, speciality):
        self.speciality = speciality

    def change_grade(self, grade):
        self.grade = self.GRADE_CHOICES[grade]

    def get_some_fields(self):
        return {
            'name': self.name,
            'status': self.status,
            'speciality': self.speciality,
            'grade': self.grade,
        }


# модель заместителя резюме
class ResumeProxy(BaseResume):
    def __init__(self, *args, **kwargs):
        self._resume = Resume(*args, **kwargs)
        self.operations = []

    def change_name(self, *args):
        func = partial(self._resume.change_name, *args)
        self.operations.append(func)

    def change_status(self, *args):
        func = partial(self._resume.change_status, *args)
        self.operations.append(func)

    def change_speciality(self, *args):
        func = partial(self._resume.change_speciality, *args)
        self.operations.append(func)

    def change_grade(self, *args):
        func = partial(self._resume.change_grade, *args)
        self.operations.append(func)

    def get_some_fields(self):
        return self._resume.get_some_fields()

    def save_changes(self):
        map(lambda f: f(), self.operations)


# модель пользователя
class AdvancedUser(object):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def add_resume(name, status_code, speciality, grade_code):
        return ResumeProxy(name, status_code, speciality, grade_code)

    def return_username(self):
        return self.username


if __name__ == '__main__':
    user = AdvancedUser('Ivan')
    user_name = user.return_username()
    first_resume = user.add_resume(user_name, 'SS', 'Front-End', 'MD')
    second_resume = user.add_resume(user_name, 'IS', 'Back-End', 'JR')
    print(user_name)
    print(first_resume.get_some_fields())
    print(second_resume.get_some_fields())
