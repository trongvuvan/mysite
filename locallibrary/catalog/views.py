from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required

from .models import Book, Author, BookInstance, Genre

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()
    num_genre = Genre.objects.count()
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre':num_genre,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
 
class BookDetailView(generic.DetailView):
    model = Book
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['copy_list'] = BookInstance.objects.all().filter(book=self.object)
        return context

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_book_list'] = Book.objects.all().filter(author=self.object)
        return context

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user, status__exact='o').order_by('due_back')
