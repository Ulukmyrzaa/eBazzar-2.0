from django.contrib import admin
from myapp.models import CustomUser
from import_export.admin import ImportExportModelAdmin

admin.site.register(CustomUser)