import django.utils.datastructures
from django.shortcuts import redirect, render
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import User, Book, DeleteRequest, Borrowedbook
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from .forms import BookForm, UserForm
from . import models
import itertools
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, logout
from django.contrib import auth, messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, "index.html")


@csrf_exempt
def signinView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            print("Hello universe")
            auth.login(request, user)
            if user.is_lib_admin or user.is_superuser:
                return render(request, 'lib_admin.html')
            else:
                books = Book.objects.all()
                return render(request, 'studenthome.html',{'books':books})
        else:
            messages.info(request, "Invalid username or password")
    return render(request, 'in.html')


def signup(request):
    return render(request, "up.html")


def signout(request):
    logout(request)
    return redirect('index.html')


def lib(request):
    return render(request, 'lib_admin.html')


def borrow(request, Book_Title, Publish_Date, Author, Publisher):
    # poor naming conventions and violating many PEPS This is bad code written in a hurry
    title = Book_Title
    published = Publish_Date
    author = Author
    publisher = Publisher
    borrower = request.user
    borrowed_book = Borrowedbook(title=title, author=author, year=published, publisher=publisher, cover="",
                                 borrower_name=borrower, borrower_email="")
    borrowed_books = Borrowedbook.objects.all()
    list_of_book_titles = []
    for book in borrowed_books:
        list_of_book_titles.append(book.title)
    if borrowed_book.title not in list_of_book_titles:
        borrowed_book.save()
        messages.success(request, "Book has been given to you for three days")
    else:
        messages.error(request, "Book Already borrowed")
    books = Book.objects.all()
    return render(request, 'studenthome.html', {'books': books})



@csrf_exempt
def registerView(request):
    if request.method == 'POST':
        requestDic = dict(request.POST)
        username = requestDic['username'][0]
        try:
            email = requestDic['email'][0]
        except:
            email = ""
        password = requestDic['password'][0]
        password = make_password(password)
        a = User(username=username, email=email, password=password)
        try:
            a.save()
            messages.success(request, 'Account was created successfully')
            print("User saved")
            books = Book.objects.all()
            return render(request, 'studenthome.html', {'books': books})
        except:
            messages.error(request, "NAME ALREADY IN SYSTEM")
            return render(request, 'in.html')
    else:
        messages.error(request, 'Registration fail, try again later')
        return redirect('signup')


# librarian_views
def librarian(request):
    book = Book.objects.all().count()
    user = User.objects.all().count()
    context = {'book': book, 'user': user}
    return render(request, 'lib_admin.html')


@login_required
def labook_form(request):
    return render(request, 'addbook.html')


@csrf_exempt
def labook(request):
    if request.method == 'POST':
        title = request.POST['title']
        author = request.POST['author']
        year = request.POST['year']
        publisher = request.POST['publisher']
        desc = request.POST['desc']
        try:
            cover = request.FILES['cover']
        except django.utils.datastructures.MultiValueDictKeyError:
            cover = ''
        current_user = request.user
        a = Book(title=title, author=author, year=year, publisher=publisher,
                 cover=cover, desc=desc, uploaded_by=current_user)
        a.save()
        messages.success(request, 'Book details uploaded successfully')
        return redirect('labook_form')
    else:
        messages.error(request, 'Book details failed to upload')
        return redirect('labook_form')


def manage(request):
    return render(request, 'librarian/base.html')


class LBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('-id')


class LManageBook(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'manage_books.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.order_by('-id')


class LDeleteView(LoginRequiredMixin, ListView):
    model = DeleteView
    template_name = 'delete_order.html'
    context_object_name = 'feedbacks'
    paginate_by = 3


def get_queryset(self):
    return DeleteRequest.objects.order_by('-id')


class LViewBook(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'bookdetails.html'


class LDeleteRequest(LoginRequiredMixin, ListView):
    model = DeleteRequest
    template_name = 'librarian/delete_order.html'
    context_object_name = 'feedbacks'
    paginate_by = 3

    def get_queryset(self):
        return DeleteRequest.objects.order_by('-id')


class LEditView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'edit_book.html'
    success_url = reverse_lazy('lmbook')
    success_message = 'Data was updated successfully'


class LDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('lmbook')
    success_message = 'Data was deleted successfully'


class LDeleteBook(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'confirm_delete2.html'
    success_url = reverse_lazy('librarian')
    success_message = 'Data was deleted successfully'


class ADeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    template_name = 'confirm_delete3.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully deleted"


class AEditUser(SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'edit_user.html'
    success_url = reverse_lazy('aluser')
    success_message = "Data successfully updated"


class ListUserView(generic.ListView):
    model = User
    template_name = 'list_users.html'
    context_object_name = 'users'
    paginate_by = 4

    def get_queryset(self):
        return User.objects.order_by('-id')


def create_user_form(request):
    choice = ['1', '0', 'lib_admin', 'students']
    choice = {'choice': choice}

    return render(request, 'adduser.html', choice)


def create_user(request):
    choice = ['1', '0', 'student', 'lib_admin']
    choice = {'choice': choice}
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        userType = request.POST['userType']
        email = request.POST['email']
        password = request.POST['password']
        password = make_password(password)
        print("User Type")
        print(userType)
        if userType == "student":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password,
                     is_publisher=True)
            a.save()
            messages.success(request, 'Member was created successfully!')
            return redirect('aluser')

        elif userType == "lib_admin":
            a = User(first_name=first_name, last_name=last_name, username=username, email=email, password=password,
                     is_librarian=True)
            a.save()
            messages.success(request, 'Member was created successfully!')
            return redirect('aluser')
        else:
            messages.success(request, 'Member was not created')
            return redirect('create_user_form')
    else:
        return redirect('create_user_form')


class ALViewUser(DetailView):
    model = User
    template_name = 'user_detail.html'


@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))
    data = query
    print(len(data))
    if (len(data) == 0):
        return redirect('librarian')
    else:
        a = data

        # Searching for It
        qs5 = models.Book.objects.filter(id__iexact=a).distinct()
        qs6 = models.Book.objects.filter(id__exact=a).distinct()

        qs7 = models.Book.objects.all().filter(id__contains=a)
        qs8 = models.Book.objects.select_related().filter(id__contains=a).distinct()
        qs9 = models.Book.objects.filter(id__startswith=a).distinct()
        qs10 = models.Book.objects.filter(id__endswith=a).distinct()
        qs11 = models.Book.objects.filter(id__istartswith=a).distinct()
        qs12 = models.Book.objects.all().filter(id__icontains=a)
        qs13 = models.Book.objects.filter(id__iendswith=a).distinct()
        files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)
        res = []
        for i in files:
            if i not in res:
                res.append(i)
        # word variable will be shown in html when user click on search button
        word = "Searched Result :"
        print("Result")
        print(res)
        files = res
        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)
        if files:
            return render(request, 'result.html', {'files': files, 'word': word})
        return render(request, 'result.html', {'files': files, 'word': word})


# student's views
@login_required
def student(request):
    books = Book.objects.all()
    return render(request, 'studenthome.html', {'books': books})


class UBookListView(LoginRequiredMixin, ListView):
    model = Book
    template_name = 'book_list.html'
    context_object_name = 'books'
    paginate_by = 2


def get_queryset(self):
    return Book.objects.order_by('-id')


@login_required
def asearch(request):
    query = request.GET['query']
    print(type(query))

    # data = query.split()
    data = query
    print(len(data))
    if (len(data) == 0):
        return redirect('student')
    else:
        a = data

        # Searching for It
        qs5 = models.Book.objects.filter(id__iexact=a).distinct()
        qs6 = models.Book.objects.filter(id__exact=a).distinct()

        qs7 = models.Book.objects.all().filter(id__contains=a)
        qs8 = models.Book.objects.select_related().filter(id__contains=a).distinct()
        qs9 = models.Book.objects.filter(id__startswith=a).distinct()
        qs10 = models.Book.objects.filter(id__endswith=a).distinct()
        qs11 = models.Book.objects.filter(id__istartswith=a).distinct()
        qs12 = models.Book.objects.all().filter(id__icontains=a)
        qs13 = models.Book.objects.filter(id__iendswith=a).distinct()

        files = itertools.chain(qs5, qs6, qs7, qs8, qs9, qs10, qs11, qs12, qs13)

        res = []
        for i in files:
            if i not in res:
                res.append(i)

        # word variable will be shown in html when user click on search button
        word = "Searched Result :"
        print("Result")

        print(res)
        files = res

        page = request.GET.get('page', 1)
        paginator = Paginator(files, 10)
        try:
            files = paginator.page(page)
        except PageNotAnInteger:
            files = paginator.page(1)
        except EmptyPage:
            files = paginator.page(paginator.num_pages)

        if files:
            return render(request, 'result.html', {'files': files, 'word': word})
        return render(request, 'result.html', {'files': files, 'word': word})
