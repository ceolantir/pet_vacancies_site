from abc import ABCMeta


# базовая модель вакансии
class Vacancy(metaclass=ABCMeta):
    def __init__(self, title, total_vacancy):
        self.title = title
        self.total_vacancy = total_vacancy
        self.verbose_name = 'Вакансия'

    def get_some_fields(self):
        return {
            'title': self.title,
            'total_vacancy': self.total_vacancy,
            'verbose_name': self.verbose_name,
        }


# базовая модель IT-вакансии
class VacancyIT(Vacancy):
    def __init__(self, title, total_vacancy):
        Vacancy.__init__(self, title, total_vacancy)
        self.verbose_name = 'IT-вакансия'


# модель по созданию Back-End вакансии
class VacancyBackEnd(VacancyIT):
    def __init__(self, total_vacancy):
        self.title = 'Back-End Разработчик'
        VacancyIT.__init__(self, self.title, total_vacancy)


# модель по созданию Front-End вакансии
class VacancyFrontEnd(VacancyIT):
    def __init__(self, total_vacancy):
        self.title = 'Front-End Разработчик'
        VacancyIT.__init__(self, self.title, total_vacancy)


# базовая модель не IT-вакансии
class VacancyNotIT(Vacancy):
    def __init__(self, title, total_vacancy):
        Vacancy.__init__(self, title, total_vacancy)
        self.verbose_name = 'не IT-вакансия'


# модель по созданию вакансии строителя
class VacancyBuilder(VacancyNotIT):
    def __init__(self, total_vacancy):
        self.title = 'Строитель'
        VacancyNotIT.__init__(self, self.title, total_vacancy)


# модель по созданию вакансии врача
class VacancyMedic(VacancyNotIT):
    def __init__(self, total_vacancy):
        self.title = 'Врач'
        VacancyNotIT.__init__(self, self.title, total_vacancy)


# базовая абстрактная фабрика по созданию базовых вакансий по направлениям
class AbstractVacancyFactory(metaclass=ABCMeta):
    # метод для создания базовой IT-вакансии
    @staticmethod
    def create_it_vacancy(title, total_vacancy):
        vacnc = VacancyIT(title=title, total_vacancy=total_vacancy)
        return vacnc.get_some_fields()

    # метод для создания базовой не IT-вакансии
    @staticmethod
    def create_not_it_vacancy(title, total_vacancy):
        vacnc = VacancyNotIT(title=title, total_vacancy=total_vacancy)
        return vacnc.get_some_fields()


# фабрика по созданию IT-вакансий
class AbstractITVacancyFactory(AbstractVacancyFactory):
    # метод для создания Back-End вакансии
    @staticmethod
    def create_backend_vacancy(total_vacancy):
        vacnc = VacancyBackEnd(total_vacancy=total_vacancy)
        return vacnc.get_some_fields()

    # метод для создания Front-End вакансии
    @staticmethod
    def create_frontend_vacancy(total_vacancy):
        vacnc = VacancyFrontEnd(total_vacancy=total_vacancy)
        return vacnc.get_some_fields()


# фабрика по созданию не IT-вакансий
class AbstractNotITVacancyFactory(AbstractVacancyFactory):
    # метод для создания вакансии строителя
    @staticmethod
    def create_builder_vacancy(total_vacancy):
        vacnc = VacancyBuilder(total_vacancy=total_vacancy)
        return vacnc.get_some_fields()

    # метод для создания вакансии врача
    @staticmethod
    def create_medic_vacancy(total_vacancy):
        vacnc = VacancyMedic(total_vacancy=total_vacancy)
        return vacnc.get_some_fields()


def conv_fields_to_str(dict):
    return f'\n{"-"*20}' \
           f'\ntitle: {dict["title"]},' \
           f'\ntotal_vacancy: {dict["total_vacancy"]},' \
           f'\nverbose_name: {dict["verbose_name"]}'


# модель пользователя
class AdvancedUser(object):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def add_it_vacancies(total_backend_vacancy, total_frontend_vacancy):
        final_vac_for_print = ''
        vacnc = AbstractITVacancyFactory()
        if total_backend_vacancy is not 0:
            final_vac_for_print += conv_fields_to_str(vacnc.create_backend_vacancy(total_backend_vacancy))
        if total_frontend_vacancy is not 0:
            final_vac_for_print += conv_fields_to_str(vacnc.create_frontend_vacancy(total_frontend_vacancy))
        return final_vac_for_print

    @staticmethod
    def add_not_it_vacancies(total_builder_vacancy, total_medic_vacancy):
        final_vac_for_print = ''
        vacnc = AbstractNotITVacancyFactory()
        if total_builder_vacancy is not 0:
            final_vac_for_print += conv_fields_to_str(vacnc.create_builder_vacancy(total_builder_vacancy))
        if total_medic_vacancy is not 0:
            final_vac_for_print += conv_fields_to_str(vacnc.create_medic_vacancy(total_builder_vacancy))
        return final_vac_for_print

    def add_vacancies(self, total_it_vacancy, total_not_it_vacancy):
        final_vac_for_print = ''
        if total_it_vacancy is not 0:
            final_vac_for_print += self.add_it_vacancies(total_it_vacancy[0], total_it_vacancy[1])
        if total_not_it_vacancy is not 0:
            final_vac_for_print += self.add_not_it_vacancies(total_not_it_vacancy[0], total_not_it_vacancy[1])
        if final_vac_for_print != '':
            return final_vac_for_print
        return 'Вакансий не создано'

    def return_username(self):
        return self.username


if __name__ == '__main__':
    user = AdvancedUser('Ivan')
    print(user.return_username())
    vacancy = user.add_vacancies([1, 2], [3, 4])
    print(f'\n{"*"*20}\n{vacancy}')
    vacancy = user.add_vacancies(0, [3, 0])
    print(f'\n{"*"*20}\n{vacancy}')
    vacancy = user.add_vacancies([1, 2], 0)
    print(f'\n{"*"*20}\n{vacancy}')
    vacancy = user.add_vacancies(0, 0)
    print(f'\n{"*"*20}\n{vacancy}')
