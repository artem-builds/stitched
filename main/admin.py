from django.contrib import admin
from .models import Category, Size, ProductSize, Product, ProductImage


# Register your models here.

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'color', 'price')
    lost_filter = ('category', 'color', 'price')
    search_fields = ('name', 'color', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductSizeInline, ProductImageInline]
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Product, ProductAdmin)
    
    

