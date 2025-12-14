class Currency():
    def __init__(self, id: str, num_code: str, char_code: str, name: str, value: float, nominal: int):
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, id: str):
        if type(id) is str and len(id) >= 6 and id[0:2] == 'R0':
            self.__id = id
        else:
            raise ValueError('Ошибка при задании уникального идентификатора валюты: id должен иметь строковое значение, хотя бы 6 символов и начинаться с R0')
    
    @property
    def num_code(self):
        return self.__num_code
    
    @num_code.setter
    def num_code(self, num_code: str):
        if type(num_code) is str and len(num_code) == 3:
            self.__num_code = num_code
        else:
            raise ValueError('Ошибка при задании num_code валюты: num_code должен иметь строковое значение, состоящее из 3 символов')

    @property
    def char_code(self):
        return self.__char_code
    
    @char_code.setter
    def char_code(self, char_code: str):
        if type(char_code) is str and len(char_code) == 3:
            self.__char_code = char_code.upper()
        else:
            raise ValueError('Ошибка при задании char_code валюты: char_code должен иметь строковое значение, состоящее из 3 символов')

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        if type(name) is str and len(name) >= 2:
            self.__name = name
        else:
            raise ValueError('Ошибка при задании имени валюты: имя должно иметь строковое значение и состоять хотя бы из 2 символов')
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value: float):
        if type(value) in (int, float):
            self.__value = float(value)
        else:
            raise TypeError('Неверный тип при задании значения валюты - должен быть тип int или float')
    
    @property
    def nominal(self):
        return self.__nominal
    
    @nominal.setter
    def nominal(self, nominal: int):
        if type(nominal) is int:
            self.__nominal = nominal
        else:
            raise TypeError('Неверный тип при задании номинала валюты - должен быть тип int')
