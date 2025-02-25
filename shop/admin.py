from django.contrib import admin
from shop.models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Category, CategoryAdmin)

class GalleryAdmin(admin.TabularInline):
    model = Gallery
    fk_name = 'product'
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title',  "price", "color", "quantity", "category"]
    list_display_links = ['title']
    list_editable = ['price', 'quantity', 'color']
    prepopulated_fields = {'slug':('title',)}
    inlines = [GalleryAdmin]

admin.site.register(Product, ProductAdmin)