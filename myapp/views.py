from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Book, Publisher, Review
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm
from django.utils import timezone

def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index0.html', {'booklist': booklist})  # passing booklist to template


def about(request):
    return render(request, 'myapp/about0.html')


# Detail view to display the details of the book
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
            else:
                choice = ' None.'
            return render(request, 'myapp/fb_results.html', {'choice': choice})
        else:
            return HttpResponse('Invalid data')
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']

            if category:
                book_list = Book.objects.filter(category=category, price__lte=max_price)
            else:
                book_list = Book.objects.filter(price__lte=max_price)

            return render(request, 'myapp/results.html', {'name': name, 'category': category, 'book_list': book_list})
        else:
            return render(request, 'myapp/findbooks.html', {'form': form, 'error': 'Invalid data'})
    else:
        form = SearchForm()
    return render(request, 'myapp/findbooks.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            form.save_m2m()
            member = order.member
            type = order.order_type
            if type == 1:
                for b in order.books.all():
                    member.borrowed_books.add(b)

            books = order.books.all()
            return render(request, 'myapp/order_response.html', {'books': books, 'order': order})
        else:
            return render(request, 'myapp/placeorder.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form})

def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            if 1 <= rating <= 5:
                review = form.save(commit=False)
                review.date = timezone.now()
                review.save()

                # Update num_reviews field in Book model
                book = review.book
                book.num_reviews += 1
                book.save()

                return redirect('myapp:index')
            else:
                form.add_error('rating', 'You must enter a rating between 1 and 5!')
        else:
            return render(request, 'myapp/review.html', {'form': form})
    else:
        form = ReviewForm()
    return render(request, 'myapp/review.html', {'form': form})