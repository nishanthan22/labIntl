from django import forms
from .models import Order, Review


class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow books'),
        ('P', 'Purchase books'),
        ('N', 'None')
    ]
    feedback = forms.MultipleChoiceField(
        choices=FEEDBACK_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Please provide your feedback"
    )


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

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'member': 'Member name'}


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'book', 'rating', 'comments']
        widgets = {'book': forms.RadioSelect()}
        labels = {
            'reviewer': 'Please enter a valid email',
            'rating': 'Rating: An integer between 1 (worst) and 5 (best)'
        }