from django.contrib import admin
from .models import Product, SubOption, Color

class SubOptionInline(admin.TabularInline):
    model = SubOption
    extra = 1

class ColorInline(admin.TabularInline):
    model = Color
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    inlines = [SubOptionInline, ColorInline]
