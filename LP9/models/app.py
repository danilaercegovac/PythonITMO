from models.author import Author

class App():
    def __init__(self, name: str, version: str, author: Author):
        self.name = name
        self.version = version
        self.author = author
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 1:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени приложения: имя должно иметь строковое значение и состоять хотя бы из 1 символа')
    
    @property
    def version(self):
        return self.__version
    
    @version.setter
    def version(self, version: str):
        if type(version) is str and len(version) >= 1:
            self.__version = version
        else:
            raise ValueError('Ошибка при задании версии приложения: версия должна иметь строковое значение и состоять хотя бы из 1 символа')
    
    @property
    def author(self):
        return self.__author
    
    @author.setter
    def author(self, author: Author):
        if isinstance(author, Author):
            self.__author = author
        else:
            raise TypeError('Неверный тип при задании автора - должен быть класс Author')