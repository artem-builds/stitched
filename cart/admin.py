from django.contrib import admin
from .models import Cart, CartItem

# Register your models here.

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('total_price', )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('session_key', 'total_items', 'subtotal', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt')
    search_fields = ('session_key',)
    inlines = [CartItemInline]
    readonly_fields = ('total_items', 'subtotal')
    
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'product_size', 'quantity', 'total_price', 'addedAt')
    list_filter = ('addedAt',)
    search_fields = ('product__name', 'cart_session_key')
    readonly_fields = ('total_price',)

