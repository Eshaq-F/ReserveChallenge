from os import system

if __name__ == '__main__':
    system("python manage.py migrate")
    system("python manage.py seed")
    system("python manage.py runserver 0.0.0.0:8000")
