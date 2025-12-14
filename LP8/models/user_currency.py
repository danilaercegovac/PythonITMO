from models.user import User
from models.currency import Currency

class User_Currency():
    def __init__(self, id: str, user_id: User, currency_id: Currency):
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id: str):
        if type(id) is str and len(id) >= 1:
            self.__id = id
        else:
            raise ValueError('Ошибка при задании уникального идентификатора отношения пользователь-валюта: id должен иметь строковое значение и состоять хотя бы из 1 символа')
    
    @property
    def user_id(self):
        return self.__user_id
    
    @user_id.setter
    def user_id(self, user_id: User):
        if isinstance(user_id, User):
            self.__user_id = user_id
        else:
            raise TypeError('Неверный тип при задании user_id - должен быть класс User')
    
    @property
    def currency_id(self):
        return self.__currency_id
    
    @currency_id.setter
    def currency_id(self, currency_id: Currency):
        if isinstance(currency_id, Currency):
            self.__currency_id = currency_id
        else:
            raise TypeError('Неверный тип при задании currency_id - должен быть класс Currency')