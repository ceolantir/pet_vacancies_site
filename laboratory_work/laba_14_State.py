from abc import ABCMeta, abstractmethod


# базовая модель статуса
class State(metaclass=ABCMeta):
    def __init__(self, self_resume):
        self.resume = self_resume
        self.status = 'NS'

    @abstractmethod
    def search_job(self, throw_result):
        raise NotImplementedError()

    def get_status(self):
        return self.status


# модель статуса: 'Не ищу работу'
class StateNS(State):
    def __init__(self, self_resume):
        State.__init__(self, self_resume)
        self.status = 'NS'

    def search_job(self, **kwargs):
        return f'Выполнение поиска работы для {self.resume.name} в соответствии со статусом {self.status}.\n' \
               'Сложная бизнес-логина, основанная на использовании сторонних ресурсов'


# модель статуса: 'Рассматриваю предложения'
class StateSS(State):
    def __init__(self, self_resume):
        State.__init__(self, self_resume)
        self.status = 'SS'

    def search_job(self, **kwargs):
        return f'Выполнение поиска работы для {self.resume.name} в соответствии со статусом {self.status}.\n' \
               'Сложная бизнес-логина, основанная на использовании сторонних ресурсов'


# модель статуса: 'Ищу работу'
class StateIS(State):
    def __init__(self, self_resume):
        State.__init__(self, self_resume)
        self.status = 'IS'

    def search_job(self, **kwargs):
        return f'Выполнение поиска работы для {self.resume.name} в соответствии со статусом {self.status}.\n' \
               'Сложная бизнес-логина, основанная на использовании сторонних ресурсов'


# модель резюме
class Resume(object):
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

    def __init__(self, name, speciality, grade_code):
        self.name = name
        self.speciality = speciality
        self.grade = self.GRADE_CHOICES[grade_code]

        self.status = StateSS(self)

    def change_name(self, name):
        self.name = name

    def change_speciality(self, speciality):
        self.speciality = speciality

    def change_grade(self, grade):
        self.grade = self.GRADE_CHOICES[grade]

    def change_state(self, state):
        self.status = state(self)

    def search(self):
        return self.status.search_job()

    def get_status(self):
        return self.status.get_status()

    def get_some_fields(self):
        return {
            'name': self.name,
            'status': self.get_status(),
            'speciality': self.speciality,
            'grade': self.grade,
        }


# модель пользователя
class AdvancedUser(object):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def add_resume(name, speciality, grade_code):
        return Resume(name, speciality, grade_code)

    def return_username(self):
        return self.username


if __name__ == '__main__':
    user = AdvancedUser('Ivan')
    user_name = user.return_username()
    resume = user.add_resume(user_name, 'Front-End', 'MD')
    print(f'{user_name}\n\n{resume.get_some_fields()}()\n{resume.search()}')

    resume.change_state(StateIS)
    resume.change_speciality('Back-End')
    resume.change_grade('TR')
    print(f'\n{resume.get_some_fields()}()\n{resume.search()}')
