import time

import django

django.setup()
from students_accounts.models import User, Borrowedbook
from django.core.mail import send_mail


def check_if_users_exceeded():
    sec_in_one_day = 60 * 60 * 24
    sec_in_three_day = 60 * 60 * 24 * 3
    sec_in_ten_day = 60 * 60 * 24 * 10
    borrowed_books = Borrowedbook.objects.all()
    user_time_dict = {}
    day_defaulters = []
    three_day_defaulters = []
    ten_day_defaulters = []
    for element in borrowed_books:
        user_time_dict.update({element.borrower_email: element.seconds_at_borrowing})
        if int(float(element.seconds_at_borrowing)) > (time.time() + sec_in_three_day) > int(
                float(element.seconds_at_borrowing)):
            day_defaulters.append(element.borrower_email)
        elif (time.time() + sec_in_three_day) < int(float(element.seconds_at_borrowing)) < (
                time.time() + sec_in_ten_day):
            three_day_defaulters.append(element.borrower_email)
        elif (time.time() + sec_in_three_day) < int(float(element.seconds_at_borrowing)):
            ten_day_defaulters.append(element.borrower_email)
        else:
            pass
        send_notification_to_users(day_defaulters, three_day_defaulters, ten_day_defaulters)


def send_notification_to_users(day_defaulters, three_day_defaulters, ten_day_defaulters):
    for user in day_defaulters:
        try:
            send_mail(
                'Reminder to return book',
                'You are kindly reminded to return the book you took today.',
                'magalareuben60@gmail.com',
                [str(user)],
                fail_silently=False,
            )
        except:
            pass
    for user in three_day_defaulters:
        try:
            send_mail(
                'Reminder to return book',
                'You are kindly required to return the book you took three days ago and bring a fine of 5000.',
                'magalareuben60@gmail.com',
                [str(user)],
                fail_silently=False,
            )
        except:
            pass
    for user in ten_day_defaulters:
        try:
            send_mail(
                'Reminder to return book',
                'You are kindly required to return the book you took ten days ago and bring a fine of 15000.',
                'magalareuben60@gmail.com',
                [str(user)],
                fail_silently=False,
            )
        except:
            pass


check_if_users_exceeded()
