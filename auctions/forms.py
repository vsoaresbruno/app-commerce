from django import forms
from .models import Category

class ListingForm(forms.Form):
    CATEGORIES = Category.objects.all().values_list("id","name")

    product_name = forms.CharField(max_length=100, label='Product name', widget=forms.TextInput(attrs={'class': "form-control"}))
    product_description = forms.CharField(label='Product description', widget=forms.Textarea(attrs={'class': "form-control"}))
    product_starting_bid = forms.DecimalField(label='Initial bid', max_value=99999, widget=forms. NumberInput(attrs={'class': "form-control"}))
    product_category = forms.ChoiceField(
        required=False,
        widget=forms.Select(attrs={'class': "form-control"}),
        choices=CATEGORIES
    )
    product_image = forms.FileField(
        required=False,
        label='Select a file',
        help_text='max. 42 megabytes',
    )
    
