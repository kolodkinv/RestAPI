# RestAPI
API для управления пользователями.

## Используемый стэк:
  - Python 2.7
  - Django REST Framework
  - Redis
  - Docker

## Запуск окружения для разработки:
  - Установите docker и docker-compose (Работоспособность проверена на docker==17.05 и docker-compose==1.20.1)
  - Перейти в папку RestAPI
  - При первом запуске выполнить команду:
  `$ docker-compose build`
  - После завершения сборки выполнить команду для поднятия контейнеров:
  `$ docker-compose up`
  - После поднятия контейнеров сервис доступен по адресу http://localhost:8000

## Описание методов:
##### GET /users?filter={} Получить список пользователей
###### Параметры:
filter=[{name}{operator}{value}] - Необязательный параметр со списком аргументов для фильтрации пользователей. Причем, {operator} - тип оператора сравнения (=, !=, >, <)
Например /users?filter=age=10 вернет пользователей с возрастом 10
###### Возращаемые значения:
HTTP 200 OK
```
{
	users : [
		{
			"surname": "SURNAME",
			"name": "NAME",
			"age": "AGE",
			"sex": "M",
			"id": "ID",
			"patronymic": "PATRONYMIC",
			"email": "EMAIL"
		}
	]
}
```

##### GET /users/{id} Получить пользователя по ИД
###### Параметры:
id - ИД пользователя
###### Возвращаемые значения
HTTP 200 OK
```
{
	users : [
		{
			"surname": "SURNAME",
			"name": "NAME",
			"age": "AGE",
			"sex": "M",
			"id": "ID",
			"patronymic": "PATRONYMIC",
			"email": "EMAIL"
		}
	]
}
```
HTTP 404 Not Found
Пользователь не найден

##### DELETE /users/{id} Удалить пользователя по ИД
###### Параметры:
id - ИД пользователя
###### Возвращаемые значения
HTTP 204 No content
Пользователь успешно удален

HTTP 404 Not Found
Пользователь не найден

##### POST /users/ Добавить пользователя
###### Параметры:
```
{
	"surname": "SURNAME",
	"name": "NAME",
	"age": "AGE",
	"sex": "M",
	"patronymic": "PATRONYMIC",
	"email": "EMAIL"
}
```
###### Возращаемые значения:
HTTP 201 Created
```
{
	"surname": "SURNAME",
	"name": "NAME",
	"age": "AGE",
	"sex": "M",
	"patronymic": "PATRONYMIC",
	"email": "EMAIL"
}
```
HTTP 400 Bad request
```
{
	name1: [ description1],
	name2: [ description2],
}
```

##### PUT /users/{id} Обновить данные пользователя
###### Параметры:
```
{
	"surname": "SURNAME",
	"name": "NAME",
	"age": "AGE",
	"sex": "M",
	"patronymic": "PATRONYMIC",
	"email": "EMAIL"
}
```
###### Возращаемые значения:
HTTP 200 OK
```
{
	"surname": "SURNAME",
	"name": "NAME",
	"age": "AGE",
	"sex": "M",
	"patronymic": "PATRONYMIC",
	"email": "EMAIL",
	"id": "ID"
}
```
HTTP 400 Bad request
Не заполнены поля
```
{
	name1: [ description1],
	name2: [ description2],
}
```

HTTP 404 Not found
Не найден пользователь

##### PATCH /users/{id} Обновить часть данных пользователя
###### Параметры:
```
{
	"surname": "SURNAME",
	"name": "NAME",
	"age": "AGE",
	"sex": "M",
	"patronymic": "PATRONYMIC",
	"email": "EMAIL"
}
```
###### Возращаемые значения:
HTTP 200 OK
```
{
	"surname": "SURNAME",
	"name": "NAME",
	"age": "AGE",
	"sex": "M",
	"patronymic": "PATRONYMIC",
	"email": "EMAIL",
	"id": "ID"
}
```
HTTP 400 Bad request
Неправильные значения полей
```
{
	name1: [ description1],
	name2: [ description2],
}
```

HTTP 404 Not found
Не найден пользователь

