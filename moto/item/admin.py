from django.contrib import admin
from .models import Category, Item

class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'created_by'] 

admin.site.register(Category)
admin.site.register(Item, ItemAdmin)