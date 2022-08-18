from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
import time


# User = get_user_model()


class User(AbstractUser):
    is_lib_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    desc = models.CharField(max_length=200, default="")
    uploaded_by = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.cover.delete()
        super().delete(*args, **kwargs)


class Borrowedbook(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    borrow_date = models.DateTimeField(auto_now=True)
    seconds_at_borrowing = models.CharField(max_length=24, default=str(time.time()))
    borrower_name = models.CharField(max_length=100, default='')
    borrower_email = models.EmailField(default='')


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.message)


class DeleteRequest(models.Model):
    delete_request = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.delete_request


class Feedback(models.Model):
    feedback = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.feedback
