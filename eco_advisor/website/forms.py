from .models import Eco

from django import forms
# forms.py

 # Import your model

class ProductSearchForm(forms.Form):
    product_name = forms.CharField(label='Product Name', max_length=100)
class packageingSearchForm(forms.Form):
    package_name = forms.CharField(label='Product package', max_length=100)