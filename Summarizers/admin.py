from django.contrib import admin
from . models import PickledModel
# Register your models here.

@admin.register(PickledModel)
class PickledModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'purpose', 'accuracy', 'uploaded_by', 'created_at', 'preprocessor', 'default')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('purpose', 'uploaded_by')
