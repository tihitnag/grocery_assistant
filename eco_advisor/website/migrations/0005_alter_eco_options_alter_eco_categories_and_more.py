# Generated by Django 4.2.8 on 2023-12-26 18:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_remove_eco_excel_file"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="eco",
            options={},
        ),
        migrations.AlterField(
            model_name="eco",
            name="categories",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="countries",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="energy",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="fruit_veg",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="eco",
            name="ingredients",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="labels",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="main_category",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="protein",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="salt",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="saturated_fat",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="eco",
            name="sugar",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
