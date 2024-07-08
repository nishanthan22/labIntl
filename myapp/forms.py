from django import forms
<<<<<<< HEAD
from .models import Order, Review

=======
from .models import Review
>>>>>>> master-clone

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
        ('O', 'Other'),
    ]
    feedback = forms.MultipleChoiceField(choices=FEEDBACK_CHOICES, widget=forms.CheckboxSelectMultiple(),
                                         label='Your feedback')


class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    name = forms.CharField(required=False, label='Your Name')
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect, required=False,
                                 label='Select a category:')
    max_price = forms.IntegerField(min_value=0, required=True, label='Maximum Price')

<<<<<<< HEAD

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'member': 'Member name'}


=======
>>>>>>> master-clone
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {'book': forms.RadioSelect()}
        labels = {
            'reviewer': 'Please enter a valid email',
            'rating': 'Rating: An integer between 1 (worst) and 5 (best)'
<<<<<<< HEAD
        }
=======
        }
>>>>>>> master-clone
