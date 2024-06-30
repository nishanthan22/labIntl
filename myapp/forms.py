from django import forms

class FeedbackForm(forms.Form):
    FEEDBACK_CHOICES = [
        ('B', 'Borrow'),
        ('P', 'Purchase'),
    ]
    feedback =   forms.ChoiceField(choices = FEEDBACK_CHOICES)
class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
        # Add more categories as needed
    ]
    name = forms.CharField(required=False, label='Your Name')
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.RadioSelect, label='Category')