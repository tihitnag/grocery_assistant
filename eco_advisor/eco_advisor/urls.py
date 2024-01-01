# eco_advisor/urls.py

from django.contrib import admin
from django.urls import path, include
from website.views import search_products,products,detail,packages,search_package  # Import the view function

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", products, name='products'),
    path("<int:pk>/", detail, name='detail'),
    path("", packages, name='packages'),
    path("", search_package, name='search_package'),
    path("", search_products, name='search_products'),  # Use an empty string for the root URL
    # ... other URL patterns ...
]
