# Generated by Django 4.2.8 on 2023-12-27 17:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0005_alter_eco_options_alter_eco_categories_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="eco",
            old_name="countries",
            new_name="categories_en",
        ),
        migrations.RemoveField(
            model_name="eco",
            name="product",
        ),
        migrations.AddField(
            model_name="eco",
            name="product_name",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="product_name"
            ),
        ),
    ]
