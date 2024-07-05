from django import forms
from .models import Customer, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields ="__all__"

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields ="__all__"
