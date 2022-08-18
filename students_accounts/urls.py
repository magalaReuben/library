from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    #path('', views.index),<<-- This was the better implementation of the url but due to interest of time i aint gonna change yours cosmos
    path('admin/', admin.site.urls),
    path('', include('students_accounts.urls')),
]

#if settings.DEBUG:
    #urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
    