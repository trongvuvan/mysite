from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from .models import Book, Author, BookInstance, Genre

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    num_authors = Author.objects.count()
    num_genre = Genre.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre':num_genre,
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
    