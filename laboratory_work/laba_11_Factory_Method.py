from abc import ABCMeta

from my_error import MyError


# базовая модель вакансии
class Vacancy(metaclass=ABCMeta):
    def __init__(self, title):
        self.verbose_name = 'Вакансия'
        self.title = title

    def return_some_fields(self):
        return {
            'title': self.title,
            'verbose_name': self.verbose_name,
        }


# базовая модель IT-вакансии
class VacancyIT(Vacancy):
    def __init__(self, title):
        Vacancy.__init__(self, title)
        self.verbose_name = 'IT-вакансия'


# базовая модель не IT-вакансии
class VacancyNotIT(Vacancy):
    def __init__(self, title):
        Vacancy.__init__(self, title)
        self.verbose_name = 'не IT-вакансия'


# фабрика
class VacancyFactory:
    @staticmethod
    def create_vacancy(is_it_company, title):
        if is_it_company == 1:
            return VacancyIT(title=title)
        elif is_it_company == 0:
            return VacancyNotIT(title=title)
        else:
            raise MyError('Ошибка с объектом класса VacancyFactory в работе с методом create_vacancy')


# модель пользователя
class AdvancedUser:
    def __init__(self, username):
        self.username = username

    @staticmethod
    def add_vacancy(is_it_company, title):
        return VacancyFactory.create_vacancy(is_it_company, title)

    def return_username(self):
        return self.username


if __name__ == '__main__':
    user = AdvancedUser('Ivan')
    first_vacancy = user.add_vacancy(0, 'Строитель')
    second_vacancy = user.add_vacancy(1, 'Тестировщик')
    print(user.return_username())
    print(first_vacancy.return_some_fields())
    print(second_vacancy.return_some_fields())
