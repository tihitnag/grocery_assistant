# eco_advisor/views.py

from django.shortcuts import render,get_object_or_404, redirect
from .forms import ProductSearchForm,packageingSearchForm
from django.db.models import Q
from .models import Eco  # Import your m
import pandas as pd

def products(request):
    
    qurey=request.GET.get('qurey',)   
    product=Eco.objects.filter()
    

    if qurey:
        product=product.filter(Q(categories_en__icontains=qurey)|Q(main_category_en__icontains=qurey))
        
    return render(request, 'core/search_prodcuts.html', {'product': product,'qurey':qurey})
def detail(request,pk):
    item=get_object_or_404(Eco,pk=pk)
    
    nutro_score,total_positive_points,total_negative_points=calculate_nutri_score_calculation(item.energy_100g,item.sugars_100g,item.saturated_fat_100g ,item.salt_100g,item.fruits_vegetables_nuts_100g,item.fiber_100g,item.proteins_100g)
    print(nutro_score)
    return render(request,'core/detail.html',{"item":item,'nutro_score':nutro_score,'total_positive_points':total_positive_points,"total_negative_points":total_negative_points})
    









    
def packages(request):
    qurey_package = request.GET.get('qurey_package',)
    print('mmkk')
    package = Eco.objects.all()  # Using all() to get all instances
    
    if qurey_package:
        package = package.filter(Q(packaging_en__icontains=qurey_package))  # Fix the typo here
    
    
    
    return render(request, 'core/search_prodcuts.html', {'package': package, 'qurey_package': qurey_package})

    
    

def search_products(request):
    if request.method == 'POST':
        form = ProductSearchForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['product_name']
            products = Eco.objects.filter(product__icontains=product_name)
            return render(request, 'core/search_results.html', {'products': products, 'form': form})
    else:
        form = ProductSearchForm()

    return render(request, 'core/search_prodcuts.html', {'form': form}) 

def search_package(request):
    print('ffff')
    if request.method == 'POST':
        form = packageingSearchForm(request.POST)
        print('mm')
        if form.is_valid():
            package = form.cleaned_data['package_name']
            package = Eco.objects.filter(packaging_en__icontains=package)
            return render(request, 'core/search_prodcuts.html', {'package': package, 'form': form})
    else:
        form = packageingSearchForm()
    

    return render(request, 'core/search_prodcuts.html', {'form': form})

def calculate_nutri_score_calculation(energy, sugars, saturated_fats, salt, fruits_vegetables, fiber, protein):
    # Your calculation function here
    # Define points thresholds for negative factors
        energy_points = [ 80, 160, 240, 320, 400, 480, 560, 640, 720, 800]
        sugars_points = [4.5, 9.0, 13.5, 18.0, 22.5, 27.0, 31.0, 36.0, 40.0, 45.0]
        saturated_fats_points = [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        salt_points = [ 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 13.5]

        # Define points thresholds for positive factors
        fruits_vegetables_points = [ 40, 60, 80]
        fiber_points = [0.7, 1.4, 2.1, 2.8, 3.5]
        protein_points = [1.6, 3.2, 4.8, 6.4, 8.0]

        # Calculate negative points

        energy_negative = next((i for i, val in enumerate(energy_points) if energy*0.239 < val), len(energy_points))
        print('energy',energy_negative)
        sugars_negative = next((i for i, val in enumerate(sugars_points) if sugars < val), len(sugars_points)) if pd.notna(sugars) else 0
        print('sugars_negative',sugars_negative)
        saturated_fats_negative = next((i for i, val in enumerate(saturated_fats_points) if saturated_fats <val), len(saturated_fats_points))if pd.notna(saturated_fats) else 0
        print('saturated_fats_negative',saturated_fats_negative)
        salt_negative = next((i for i, val in enumerate(salt_points) if salt < val), len(salt_points)) if pd.notna(salt) else 0
        print('salt_negative',salt_negative)
        total_negative_points = sum([energy_negative, sugars_negative, saturated_fats_negative, salt_negative])

        # Calculate positive points

        if fruits_vegetables is not None:
            if fruits_vegetables < 40:
                fruits_vegetables_positive = 0
            elif 40 <= fruits_vegetables < 60:
                fruits_vegetables_positive = 1
            elif 60 <= fruits_vegetables < 80:
                fruits_vegetables_positive = 2
            elif fruits_vegetables >= 80:
                fruits_vegetables_positive = 5
            else:
                fruits_vegetables_positive = 0
        else:
    # Handle the case where fruits_vegetables is None (customize as needed)
            fruits_vegetables_positive = 0  # or another appropriate value

        fiber_positive = next((i for i, val in enumerate(fiber_points) if fiber < val), len(fiber_points)) if pd.notna(fiber) else 0

        print('fiber',fiber_positive)
        protein_positive = next((i for i, val in enumerate(protein_points) if protein < val), len(protein_points)) if pd.notna(protein) else 0
        print('protien',protein_positive)
        total_positive_points = sum([fruits_vegetables_positive, fiber_positive, protein_positive])
        print('postive',total_positive_points)
        print('negative',total_negative_points)
        # Calculate Nutri-Score
        #The points for proteins are not counted because the negative points are greater or equal to 11.
        if total_negative_points>=11:
            nutri_score = total_negative_points - (total_positive_points-protein_positive)
            print("with out protin ",nutri_score)
            return  nutri_score,total_positive_points,total_negative_points
        else:
            nutri_score=total_negative_points-total_positive_points
            print(total_negative_points)
            print(total_positive_points)
            return nutri_score,total_positive_points,total_negative_points




            