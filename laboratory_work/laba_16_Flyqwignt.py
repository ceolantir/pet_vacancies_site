class Skill(object):
    def __init__(self, title):
        self.title = title


class SkillFactory:
    skills = {}

    @staticmethod
    def get_skill(title):
        return SkillFactory.skills.setdefault(title, Skill(title))


# модель пользователя
class AdvancedUser(object):
    def __init__(self, username):
        self.username = username

    def assign_skill(self, title):
        skill = SkillFactory.get_skill(title)
        print("{} - skill {} [{}]".format(self.username, skill.title, id(skill)))

    def return_username(self):
        return self.username


if __name__ == '__main__':
    AdvancedUser('Ivan').assign_skill('Python')
    AdvancedUser('Ivan').assign_skill('JS')
    print('\n')
    AdvancedUser('Vlad').assign_skill('Python')
    AdvancedUser('Vlad').assign_skill('REST')
    print('\n')
    AdvancedUser('Oleg').assign_skill('Python')
    AdvancedUser('Oleg').assign_skill('SQL')
    print('\n')
    AdvancedUser('Tamir').assign_skill('Python')
    AdvancedUser('Tamir').assign_skill('JS')
    AdvancedUser('Tamir').assign_skill('REST')
    AdvancedUser('Tamir').assign_skill('SQL')
