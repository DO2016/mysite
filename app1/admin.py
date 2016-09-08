from django.contrib import admin

# Register your models here.

from .models import ModelTable

admin.site.register(ModelTable)