# eco_advisor/views.py

from django.shortcuts import render,get_object_or_404, redirect
from .forms import ProductSearchForm
from django.db.models import Q
from .models import Eco  # Import your m
import pandas as pd


def products(request):
    
    qurey=request.GET.get('qurey',)  
    qurey_package = request.GET.get('qurey_package',) 
    product=Eco.objects.filter()
    
    
    if qurey and qurey_package :
        product=product.filter(Q(categories_en__icontains=qurey) & (Q(packaging_en__icontains=qurey_package)))
  
    return render(request, 'core/search_prodcuts.html', {'product': product,'qurey':qurey, 'qurey_package': qurey_package})

def detail(request,pk):
    item=get_object_or_404(Eco,pk=pk)
   
    product=Eco.objects.filter()
    catagory=Eco.objects.filter(Q(main_category_en__icontains=item.main_category_en)).order_by("NutriScore") [:5]
    for i in catagory:
        
        print("mmmmmmmmmm",i.NutriScore,i.product_name)
    
    nutro_score,total_positive_points,total_negative_points,energy_negative,sugars_negative,saturated_fats_negative,salt_negative,fruits_vegetables_positive,fiber_positive,protein_positive=clculate_nutri_score_calculation(item.energy_100g,item.sugars_100g,item.saturated_fat_100g ,item.salt_100g,item.fruits_vegetables_nuts_100g,item.fiber_100g,item.proteins_100g)
    print(nutro_score)
    package1=calculate(item.packaging_en.lower())
    print(package1,"package ")
    
    
    return render(request,'core/detail.html',{"item":item,'nutro_score':nutro_score,'total_positive_points':total_positive_points,"total_negative_points":total_negative_points,'energy_negative':energy_negative,'sugars_negative':sugars_negative,'saturated_fats_negative':saturated_fats_negative,'salt_negative':salt_negative,'fiber_positive':fiber_positive,"protein_positive":protein_positive,"fruits_vegetables_positive":fruits_vegetables_positive,"package1":package1})
     
# def packages(request):
#     print('mmmm')
#     qurey_package = request.GET.get('qurey_package',)
#     print('mmkk')
#     package = Eco.objects.all()  # Using all() to get all instances
    
#     if qurey_package:
#         package = package.filter(Q(packaging_en__icontains=qurey_package))  # Fix the typo here
    
    
    
#     return render(request, 'core/search_prodcuts.html', {'package': package, 'qurey_package': qurey_package})

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

def clculate_nutri_score_calculation(energy, sugars, saturated_fats, salt, fruits_vegetables, fiber, protein):
    # Your calculatioan function here
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
            return  nutri_score,total_positive_points,total_negative_points,energy_negative,sugars_negative,saturated_fats_negative,salt_negative,fiber_positive,protein_positive,fruits_vegetables_positive
        else:
            nutri_score=total_negative_points-total_positive_points
            print(total_negative_points)
            print(total_positive_points)
            return nutri_score,total_positive_points,total_negative_points,energy_negative,sugars_negative,saturated_fats_negative,salt_negative,fiber_positive,protein_positive,fruits_vegetables_positive

def assign_letter_grade(nutri_score):
    if nutri_score<0:
        return 'A'
    elif 0 <= nutri_score <= 2:
        return 'B'
    elif 3 <= nutri_score <= 10:
        return 'C'
    elif 11 <= nutri_score <= 18:
        return 'D'
    else:
        return 'E'
    
    
    
    #canculating eco score 
def classify_material(material):
    
    paper_types = ['tetrapak', 'tetra brik', 'carton', 'fcs paper', 'cardboard', 'wood']
    metal_types = ['steel cans', 'steel triplate', '41 aluminum light', '90 aluminum heavy']
    glass_types = ['70 gl', '71 gl', '97 gl']
    plastic_types = ['pvc', 'ldpe', 'pp 5', 'pp 05', '05 pp', 'ps 06', 'pap 05', 'hdpe', 'pe-ld04', 'pet', 'plastic']
    for paper_type in paper_types:
        if paper_type in material:
            return 'Paper', material
    for metal_type in metal_types:
        if metal_type in material:
            return 'Metal', material
    for plastic_type in plastic_types:
        if plastic_type in material:
            return 'Plastic', material
    for glass_type in glass_types:
        if glass_type in material:
            return 'Glass', material
    return 'Unknown', material

def determine_material_type(item):
    paper_types = ['tetrapak', 'tetra brik', 'carton', 'fcs paper', 'cardboard', 'wood']
    metal_types = ['steel cans', 'steel triplate', '41 aluminum light', '90 aluminum heavy']
    glass_types = ['70 gl', '71 gl', '97 gl']
    plastic_types = ['pvc', 'ldpe', 'pp 5', 'pp 05', '05 pp', 'ps 06', 'pap 05', 'hdpe', 'pe-ld04', 'pet', 'plastic']

    if isinstance(item, str):
        for paper_type in paper_types:
            if paper_type in item:
                return 'Paper', paper_type
        for metal_type in metal_types:
            if metal_type in item:
                return 'Metal', metal_type
        for glass_type in glass_types:
            if glass_type in item:
                return 'Glass', glass_type
        for plastic_type in plastic_types:
            if plastic_type in item:
                return 'Plastic', plastic_type
    return 'Unknown', "unknown"

def calculate_eco_score(material_data):
    eco_scores = []
    for upstream, downstream, penalty in zip(material_data['Upstream'], material_data['Downstream'],
                                             material_data['Penalty']):
        eco_score = (upstream + downstream) / 2 - penalty
        eco_scores.append(eco_score)
    return eco_scores

def grade_material(eco_scores):
    grades = []
    for eco_score in eco_scores:
        if 0 <= eco_score < 20:
            grades.append('E')
        elif 20 <= eco_score < 40:
            grades.append('D')
        elif 40 <= eco_score < 60:
            grades.append('C')
        elif 60 <= eco_score < 80:
            grades.append('B')
        elif 80 <= eco_score <= 100:
            grades.append('A')
        else:
            return 'Out of Range'
    return grades

def analyze_material(material_data, material_type, category):
    eco_scores = calculate_eco_score(material_data)
    grades = grade_material(eco_scores)

    for i, material in enumerate(material_data['Material']):
        if material == category:
            return material, material_type, category, eco_scores[i], grades[i]

# Data for different materials
glass_data = {
    'Material': ['70 gl', '71 gl', '97 gl'],
    'Upstream': [61, 61, 61],
    'Downstream': [100, 100, 100],
    'Penalty': [2, 2, 2]
}

paper_data = {
    'Material': ['tetrapak', 'tetra brik', 'carton', 'fcs paper', 'cardboard', 'wood'],
    'Upstream': [49, 56, 100, 92, 83, 50],
    'Downstream': [75, 80, 100, 98, 103, 50],
    'Penalty': [4, 3, 0, 0, 1, 5]
}

metal_data = {
    'Material': ['steel cans', 'steel triplate', '41 aluminum light', '90 aluminum heavy'],
    'Upstream': [51, 51, 44, 44],
    'Downstream': [100, 100, 28, 100],
    'Penalty': [2, 2, 6, 3]
}

plastic_data = {
    'Material': ['pvc', 'ldpe', 'pp 5', 'pp 05', '05 pp', 'ps 06', 'pap 05', 'hdpe', 'pe-ld04', 'pet', 'plastic'],
    'Upstream': [0, 15, 15, 0, 0, 25, 15, 50, 50, 100, 50],
    'Downstream': [20, 41, 41, 20, 20, 41, 41, 31, 41, 100, 20],
    'Penalty': [10, 8, 8, 10, 10, 8, 8, 5, 8, 0, 8]
}

# Create DataFrames
glass_df = pd.DataFrame(glass_data)
paper_df = pd.DataFrame(paper_data)
metal_df = pd.DataFrame(metal_data)
plastic_df = pd.DataFrame(plastic_data)

# Store the results in a list
def calculate(package1):
        all_results = []
    
   
        material_type, category = determine_material_type(package1.lower())
        if material_type != 'Unknown':
            if material_type == 'Glass':
                result = analyze_material(glass_df, material_type, category)
            elif material_type == 'Paper':
                result = analyze_material(paper_df, material_type, category)
            elif material_type == 'Metal':
                result = analyze_material(metal_df, material_type, category)
            elif material_type == 'Plastic':
                result = analyze_material(plastic_df, material_type, category)
            else:
                print(f"Unknown material type: {material_type}, Category: {category}")
        else:
            # Handle the case when material type is 'Unknown'
            result = ('Unknown', 'Unknown', 'Unknown', 'Unknown', 0)
        return result
       
        all_results.append(result)

# recomnndation  
