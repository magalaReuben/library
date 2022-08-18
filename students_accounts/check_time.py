from django.apps import AppConfig
from students_accounts.models import User, Borrowedbook


class CheckIfUserExceededTime(AppConfig):
    print("Running")
    name = 'library_system'
    verbose_name = "MyApplication"
    def ready(self):
        check_if_user_exceeded()


def check_if_user_exceeded():
    sec_in_one_day = 60 * 60 * 24
    sec_in_three_day = 60 * 60 * 24 * 3
    borrowed_books = Borrowedbook.objects.all()
    user_time_dict = {}
    for element in borrowed_books:
        print(element)
