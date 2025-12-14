class User():
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id: str):
        if type(id) is str and len(id) >= 1:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании уникального идентификатора пользователя: id должен иметь строковое значение и состоять хотя бы из 1 символа')
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени пользователя: имя должно иметь строковое значение и состоять хотя бы из 2 символов')
    
    