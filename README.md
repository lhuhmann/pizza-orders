# Useful things

* tutorial: https://docs.djangoproject.com/en/3.1/intro/tutorial01/
* To launch app and specify a port: `python manage.py runserver 8080`
* to generate migration: `python manage.py makemigrations <appname>`
* to view migration as SQL: `python manage.py sqlmigrate <appname> <migrationnum>`
* to run all migrations that haven't been applied: `python manage.py migrate`
* to check for problems in project: `python manage.py check`

* repo is for a Django project (pizza)
* projects can contain multiple apps; I've added the app 'orders' to handle ordering

# Steps taken to create database
1. Create models.py
2. Run python manage.py makemigrations orders
3. Run python manage.py migrate
4. Create 0002_load_data.py to define migration to load data into the app
5. Run python manage.py migrate to load data into app
6. Run winpty python manage.py createsuperuser to add a user who can view admin interface
7. To inspect the database locally, one option is to install DB Browser for SQLLite
