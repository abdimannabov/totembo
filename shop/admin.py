from django.contrib import admin
from shop.models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'get_count']
    list_display_links = ['id', 'title']
    prepopulated_fields = {'slug':('title',)}
    def get_count(self, obj):
        if obj.products:
            return str(len(obj.products.all()))
        else:
            return "0"
    get_count.short_description = "Product Count"

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
admin.site.register(Like)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(ShippingAddress)
