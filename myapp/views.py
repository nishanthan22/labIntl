from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
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


def about(request):
    response = HttpResponse()
    heading1 = '<p>' + 'This is an eBook Website ' + '</p>'
    response.write(heading1)
    return response


#Detail view to display the details of the book
def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)  # This will raise a 404 error if the book does not exist
    details_response = HttpResponse()
    details_response.write('<h1>Details of the book with id #' + str(book_id) + '</h1>')
    book_name = book.title.upper()
    book_price = book.price
    book_publisher = book.publisher.name
    details_response.write('<p> The ' + book_name + ' costs $' + str(book_price) + ' and, published by '
                           + book_publisher + '</p>')
    return details_response
