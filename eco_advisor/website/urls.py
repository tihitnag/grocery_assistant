# urls.py
from django.urls import path
from .views import search_products,navbar
from . import views
app_name="item"
urlpatterns = [
     path(' ', views.search_products, name='search_products'),
     path("navbar/", navbar, name='navbar'), 
     
    # Add other URL patterns as needed
]

