from django.contrib import admin
from .models import User, Book, Chat, DeleteRequest, Feedback, Borrowedbook

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(DeleteRequest)
admin.site.register(Feedback)
admin.site.register(Borrowedbook)

