class Author():
    def __init__(self, name: str, group: str):
        self.name = name
        self.group = group

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени автора: имя должно иметь строковое значение и состоять хотя бы из 2 символов')

    @property
    def group(self):
        return self.__group

    @group.setter
    def group(self, group: str):
        if type(group) is str and len(group) >= 5:
            self.__group = group
        else:
            raise ValueError('Ошибка при задании группы автора: группа должна иметь строковое значение и состоять хотя бы из 5 символов')