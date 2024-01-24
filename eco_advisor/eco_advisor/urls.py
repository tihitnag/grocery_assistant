# eco_advisor/urls.py

from django.contrib import admin
from django.urls import path, include
from website.views import search_products,products,detail,search_package,navbar# Import the view function
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", products, name='products'),
    path("<int:pk>/", detail, name='detail'),
    path("navbar/", navbar, name='navbar'),  # Added a distinct path for packages
    path("search_package/", search_package, name='search_package'),  # Distinct path for search_package
    path("search_products/", search_products, name='search_products'),  # Distinct path for search_products
    # ... other URL patterns ...
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
