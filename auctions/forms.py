from decimal import Decimal
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Category, Listing

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = (
            'name',
            'description',
            'price',
            'upload',
            'category',
        )
        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control"}),
            'description': forms.Textarea(attrs={'class': "form-control"}),
            'price': forms. NumberInput(attrs={'class': "form-control"}),
            'category': forms.Select(attrs={'class': "form-control"}),
        }
        labels = {
            'name': _('Product name'),
            'description': _('Product description'),
            'price': _('Initial bid'),
            'upload': _('Select a file'),
        }
        help_texts = {
            'upload': _('max. 42 megabytes'),
        }

    # Validação "manual" do campo
    # esse método será chamado pelo is_valid
    # o padrão é sempre clean_<field_name>
    # se algo estiver errado, basta dar um raise forms.ValidationError("Alguma mensagem")
    def clean_price(self):
        # é um objeto Decimal pq na model é um DecimalField
        price = self.cleaned_data['price']
        # aproxima pra duas casas decimais
        return price.quantize(Decimal('1.00'))
