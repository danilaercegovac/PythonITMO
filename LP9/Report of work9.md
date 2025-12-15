# Лабораторная работа №9   
**Тема:** Реализация CRUD-операций с использованием архитектуры MVC и SQLite (в памяти)

---

## 1. Цель работы

Целью данной лабораторной работы является:

- Реализация CRUD (Create, Read, Update, Delete) операций для сущностей бизнес-логики приложения.
- Освоение работы с базой данных SQLite, размещённой в оперативной памяти (`:memory:`).
- Изучение принципов первичных и внешних ключей и их роли в связях между таблицами.
- Применение архитектурного паттерна MVC (Model–View–Controller).
- Разделение ответственности между слоями приложения.
- Реализация маршрутизации HTTP-запросов.
- Отображение данных пользователю с использованием шаблонов Jinja2.
- Написание модульных тестов с применением `unittest` и `unittest.mock`.

---

## 2. Описание моделей и их связей

### 2.1 Модель Author (`models/author.py`)

Модель описывает автора приложения.

**Свойства:**
- `name` — имя автора (строка, не менее 2 символов)
- `group` — учебная группа (строка, не менее 5 символов)

Проверка корректности значений выполняется через геттеры и сеттеры.

---

### 2.2 Модель App (`models/app.py`)

Модель хранит информацию о приложении.

**Свойства:**
- `name` — название приложения
- `version` — версия приложения
- `author` — объект класса `Author`

---

### 2.3 Модель Currency (`models/currency.py`)

Модель описывает валюту.

**Свойства:**
- `id` — уникальный идентификатор валюты
- `num_code` — числовой код валюты
- `char_code` — буквенный код валюты
- `name` — название валюты
- `value` — курс валюты
- `nominal` — номинал

---

### 2.4 Связи между сущностями в базе данных

В базе данных реализованы следующие таблицы:

```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    num_code TEXT NOT NULL,
    char_code TEXT NOT NULL,
    name TEXT NOT NULL,
    value FLOAT,
    nominal INTEGER
);

CREATE TABLE user_currency (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    currency_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(currency_id) REFERENCES currency(id)
);
`````
Таблица user_currency реализует связь «многие-ко-многим» между пользователями и валютами.

## 3. Структура проекта

LP9/
├── controllers/
│   ├── databasecontroller.py   # Работа с SQLite (CRUD)
│   ├── currencycontroller.py   # Бизнес-логика валют
│   └── pages.py                # Рендеринг HTML-страниц
│
├── models/
│   ├── author.py               # Модель автора
│   ├── app.py                  # Модель приложения
│   └── currency.py             # Модель валюты
│
├── templates/
│   ├── index.html               # Главная страница
│   ├── author.html              # Информация об авторе
│   ├── currencies.html          # Таблица валют
│   └── error.html               # Страница ошибки
│
├── tests/
│   ├── test_databasecontroller.py
│   ├── test_currencycontroller.py
│   ├── test_pages.py
│   └── test_routes.py
│
├── currencies_api.py            # Получение курсов валют из API ЦБ РФ
├── myapp.py                     # Точка входа и маршрутизация
├── screenshots/
│   ├── main_page.png # Скриншот главной страницы
│   ├── author_page.png # Скриншот author страницы
│   ├── currencies_page.png # Скриншот currencies страницы
│   ├── currencies_create_page.png # Скриншот currencies страницы с созданной строкой
│   ├── currencies_delete_page.png # Скриншот currencies страницы с удалённой строкой
│   └── currencies_update_page.png # Скриншот currencies страницы с обновлённой строкой
└── venv/                        # Виртуальное окружение

## 4. Реализация CRUD и примеры SQL-запросов

### 4.1 Create (Добавление валюты)

```sql
INSERT INTO currency(num_code, char_code, name, value, nominal)
VALUES(:num_code, :char_code, :name, :value, :nominal);
```

---

### 4.2 Read (Чтение данных)

```sql
SELECT * FROM currency;
```

```sql
SELECT * FROM currency WHERE char_code = ?;
```

---

### 4.3 Update (Обновление курса валюты)

```sql
UPDATE currency SET value = ? WHERE char_code = ?;
```

---

### 4.4 Delete (Удаление валюты)

```sql
DELETE FROM currency WHERE id = ?;
```

---

## 5. Примеры URL-запросов приложения

| URL | Назначение |
|----|-----------|
| `/` | Главная страница |
| `/author` | Информация об авторе |
| `/currencies` | Таблица валют |
| `/currency/create?char_code=USD&name=Dollar&num_code=840` | Добавление валюты |
| `/currency/update?USD=91.5` | Обновление курса валюты |
| `/currency/delete?id=1` | Удаление валюты |
| `/currency/show` | Вывод валют в консоль |

---

## 6. Примеры тестирования с использованием unittest.mock

```python
@patch("controllers.currencycontroller.get_currencies")
def test_create_currency_success(self, mock_get):
    mock_get.return_value = {"USD": "90,5"}
    self.controller.create_currency("USD", "Dollar", "840")
    self.mock_crud.create_one.assert_called_once()
```

---

## 7. Выводы

В ходе выполнения лабораторной работы была реализована архитектура MVC, освоена работа с SQLite в памяти, реализованы CRUD-операции, маршрутизация HTTP-запросов и рендеринг HTML-шаблонов.  
Использование MVC позволило повысить читаемость, тестируемость и масштабируемость приложения.
