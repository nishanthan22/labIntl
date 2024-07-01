from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Book, Publisher
from django.shortcuts import render
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist})  # passing booklist to template

def about(request):
    return render(request, 'myapp/about0.html')

#Detail view to display the details of the book
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'myapp/detail0.html', {'book': book})

def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            if feedback == 'B':
                choice = ' to borrow books.'
            elif feedback == 'P':
                choice = ' to purchase books.'
            else: choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice':choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form':form})

def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            booklist = Book.objects.filter(category=category)  # Assuming Book model has a category field
            return render(request, 'myapp/results.html', {'name': name, 'booklist': booklist})
        else:
            return render(request, 'myapp/findbooks.html', {'form': form, 'error': 'Invalid data'})
    else:
        form = SearchForm()
    return render(request, 'myapp/findbooks.html', {'form': form})