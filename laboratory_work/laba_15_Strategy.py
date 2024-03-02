from abc import ABCMeta, abstractmethod


# базовая модель стратегии
class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def sending(self, data):
        raise NotImplementedError()


# модель отправки приложения отклика выбранной компании
class StrategySendingToOne(Strategy):
    def sending(self, data):
        # отправляем выбранной компании
        return f'Отправили определенной компании'


# модель отправки приложения отклика подходящим компаниям по переданным параметрам
class StrategySendingYoMultiple(Strategy):
    def sending(self, data):
        # отправляем по сложной логике
        return 'Отправили всем, кто подходит'


# модель приложения отклика на вакансию
class Application(object):
    def __init__(self, name, phone, strategy):
        self.name = name
        self.phone = phone
        self.verbose_name = 'Отклик'

        self.strategy = strategy()

    def get_some_fields(self):
        return {
            'name': self.name,
            'phone': self.phone,
        }

    def change_state(self, strategy):
        self.strategy = strategy()

    def sending_app(self):
        return self.strategy.sending(self.get_some_fields())


# модель пользователя
class AdvancedUser(object):
    def __init__(self, username):
        self.username = username

    @staticmethod
    def add_application(name, phone, strategy):
        return Application(name, phone, strategy)

    def return_username(self):
        return self.username


if __name__ == '__main__':
    user = AdvancedUser('Ivan')
    user_name = user.return_username()
    application = user.add_application(user_name, 81234567890, StrategySendingToOne)
    print(f'{user_name}\n\n{application.get_some_fields()}\n{application.sending_app()}')

    application.change_state(StrategySendingYoMultiple)
    print(f'\n{application.get_some_fields()}\n{application.sending_app()}')
