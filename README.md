# Useful things

* tutorial: https://docs.djangoproject.com/en/3.1/intro/tutorial01/
* To launch app and specify a port: `python manage.py runserver 8080`
* to generate migration: `python manage.py makemigrations <appname>`
* to view migration as SQL: `python manage.py sqlmigrate <appname> <migrationnum>`
* to run all migrations that haven't been applied: `python manage.py migrate`
* to check for problems in project: `python manage.py check`