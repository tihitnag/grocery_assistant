from django.db import models

class Eco(models.Model):
    product_name = models.CharField('product_name',max_length=30, null=True, blank=True)
    categories_en = models.CharField( max_length=30, null=True, blank=True)
    countries_en = models.CharField( max_length=30, null=True, blank=True)
    packaging_en = models.CharField( max_length=30,null=True, blank=True)
    labels_en = models.CharField( max_length=30,null=True, blank=True)
    ingredients_text = models.CharField( max_length=30, null=True, blank=True)
    main_category_en = models.CharField( max_length=30, null=True, blank=True)
    energy_100g = models.FloatField( null=True, blank=True)
    image_url = models.ImageField( null=True, blank=True)
    saturated_fat_100g = models.FloatField( null=True, blank=True)
    sugars_100g = models.FloatField( null=True, blank=True)
    proteins_100g = models.FloatField( null=True, blank=True)
    salt_100g = models.FloatField( null=True, blank=True)
    fruits_vegetables_nuts_100g = models.FloatField( null=True, blank=True)
    fiber_100g=models.FloatField( null=True, blank=True)
 
    class Meta:
        db_table = 'eco'
