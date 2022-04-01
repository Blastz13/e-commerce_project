# Установка и настройка

**Установка**

Вы можете склонировать данное приложение:

```bash
git clone https://github.com/Blastz13/e-commerce_project.git
```

Далее, нужно установить нужные библиотеки

```bash
pip3 install -r requirements.txt
```

**Настройка**

Перейдите в каталог веб-приложения, создайте миграции и соберите статику.

```bash
cd tree_emploes
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
```

Также, вы можете создать супер-юзера. Это делается с помощью команды:

```bash
python3 manage.py createsuperuser
```

Теперь вы можете запускать сервер.

```bash
python3 manage.py runserver
```

### Работа веб-приложения

```url
admin/ - Переход в админку
api/v1/list-subdivision/ - Вывод всех подразделений**
api/v1/list-subdivision-emploe/<int:pk> - Вывод сотрудников конкретного подразделения***
api/v1/detail-emploe/<int:pk> - Вывод информации о сотруднике
api/v1/detail-emploe/<int:pk>/subordinate - Вывод подчиненных сотрудников
```

** - Поддерживает флаг ?reverse=True или False для сортировки по полю Название в прямом и обратном порядке

*** - Поддерживает флаг ?reverse=True или False для сортировки по полю ФИО в прямом и обратном порядке

Теперь вы успешно можете пользоваться 


### Лицензия

Copyright © 2021 [Blastz13](https://github.com/Blastz13/).