from django.http import HttpResponse
from .models import Book, Publisher


def index(request):
    response = HttpResponse()

    # Get the list of books ordered by primary key
    booklist = Book.objects.all().order_by('id')

    # Get the list of publishers ordered by city name in descending order
    publisherlist = Publisher.objects.all().order_by('-city')

    # Add books to response
    response.write('<h1>List of Books</h1>')
    for book in booklist:
        response.write(f'<p>{book.id}. {book.title}</p>')

    # Add publishers to response
    response.write('<h1>List of Publishers</h1>')
    for publisher in publisherlist:
        response.write(f'<p>{publisher.name} located in {publisher.city}</p>')

    return response


