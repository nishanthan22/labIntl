from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Book, Review
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import FeedbackForm, SearchForm, OrderForm, ReviewForm
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Avg
import random


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]

    # Checking if last_login exists in session
    last_login = request.session.get('last_login')
    if last_login:
        message = f"Your last login was at {last_login}."
    else:
        message = "Your last login was more than one hour ago."

    return render(request, 'myapp/index0.html', {'booklist': booklist, 'message': message})

def about(request):
    lucky_num = request.COOKIES.get('lucky_num')
    if lucky_num:
        mynum = int(lucky_num)
    else:
        # Generate a random number between 1 and 100
        mynum = random.randint(1, 100)

    # Prepare the response
    response = render(request, 'myapp/about0.html', {'mynum': mynum})

    # Set the cookie to expire after 5 minutes using max_age
    max_age = 5 * 60  # 5 minutes in seconds
    response.set_cookie('lucky_num', mynum, max_age=max_age)

    return response


# Detail view to display the details of the book
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'myapp/detail0.html', {'book': book})


def getFeedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            choices = []
            if 'B' in feedback:
                choices.append('to borrow books')
            if 'P' in feedback:
                choices.append('to purchase books')
            if 'N' in feedback:
                choices.append('None')

            return render(request, 'myapp/fb_results.html', {'choices': choices})
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
            min_price = form.cleaned_data['min_price']

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


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
                request.session.set_expiry(3600)  # 1 hour expiry
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('myapp:index'))


@login_required
def chk_reviews(request, book_id):
    user = request.user
    book = get_object_or_404(Book, pk=book_id)
    if user.groups.filter(name='Member').exists():
        reviews = Review.objects.filter(book=book)
        if reviews.exists():
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            return render(request, 'myapp/chk_reviews.html', {'avg_rating': avg_rating, 'book': book})
        else:
            return render(request, 'myapp/chk_reviews.html', {'message': 'No reviews submitted for this book.'})
    else:
        return render(request, 'myapp/chk_reviews.html', {'message': 'You are not a registered member!'})