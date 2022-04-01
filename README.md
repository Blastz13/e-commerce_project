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
cd e-commerce_project
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

### Лицензия

Copyright © 2021 [Blastz13](https://github.com/Blastz13/).
