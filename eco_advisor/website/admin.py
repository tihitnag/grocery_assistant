from django.contrib import admin

from .models import Eco


from import_export.admin import ImportExportActionModelAdmin
@admin.register(Eco)
class userdat(ImportExportActionModelAdmin):
    pass

# Register your models here.
