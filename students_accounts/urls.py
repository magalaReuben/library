from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('signin/', views.signinView, name='signin'),
    path('signin/addbook', views.labook, name='addbook'),
    path('signin/signin', views.signinView, name='signin'),
    path('logout', views.signout, name='logout'),
    path('signin/in.html', views.signinView, name='signin'),
    path('signin/signup/signin', views.registerView, name='signup'),
    path('signin/signup/', views.signup, name='signup'),
    path('signin/logout', views.signup, name='logout'),
    path('borrow', views.borrow, name='borrow'),
    path('signin/borrow/<str:Book_Title>/<str:Publish_Date>/<str:Author>/<str:Publisher>', views.borrow, name='borrow'),
    path('signin/signup/signup', views.signup, name='signup'),
    path('addbooks', views.labook, name='addbook'),
    path('signout/', views.signout, name='signout'),
    path('lib/', views.lib, name='lib'),

    # Librarian URLs
    path('librarian/', views.librarian, name='librarian'),
    path('labook_form/', views.labook_form, name='labook_form'),
    path('labook/', views.labook, name='labook'),
    path('signin/llbook', views.manage, name="manage"),
    path('labook_form/addbook', views.labook, name='labook'),
    path('lrbook', views.LBookListView.as_view(), name='lrbook'),
    path('llbook/', views.LBookListView.as_view(), name='llbook'),
    path('librarian/llbook', views.manage, name="manage"),
    path('lmbook/', views.LManageBook.as_view(), name='lmbook'),
    path('librarian/addbook', views.labook, name="labook"),
    path('ldrequest/', views.LDeleteRequest.as_view(), name='ldrequest'),
    # path('ldorder/', views.DeleteRequest.as_view(), name='ldorder'),
    path('lvbook/<int:pk>', views.LViewBook.as_view(), name='lvbook'),
    path('lebook/<int:pk>', views.LEditView.as_view(), name='lebook'),
    path('ldbookk/<int:pk>', views.LDeleteView.as_view(), name='ldbookk'),
    path('librarian/ldbook/<int:pk>', views.LDeleteBook.as_view(), name='ldbook'),
    path('aduser/<int:pk>', views.ADeleteUser.as_view(), name='aduser'),
    path('aeuser/<int:pk>', views.AEditUser.as_view(), name='aeuser'),
    path('aluser', views.ListUserView.as_view(), name='aluser'),
    path('llbook/aluser', views.ListUserView.as_view(), name='aluser'),
    path('ldrequest/aluser', views.ListUserView.as_view(), name='aluser'),
    path('create_user_form/', views.create_user_form, name='create_user_form'),
    path('create_user/', views.create_user, name='create_user'),
    path('alvuser/<int:pk>', views.ALViewUser.as_view(), name='alvuser'),
    path('asearch/', views.asearch, name='asearch'),

    # students' url(
    path('student', views.student, name='student'),
    path('asearch/', views.asearch, name='asearch'),

]
