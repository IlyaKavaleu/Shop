from django.contrib import admin
from .models import Category, Product, User, Cart, CartItem

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(CartItem)


class CartItemAdmin(admin.TabularInline):
    model = CartItem
    fields = ('product', 'cart', 'quantity', 'active')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    model = Cart
    fields = ('date_added', 'user')
    readonly_fields = ('date_added',)
    extra = 0
    inlines = (CartItemAdmin,)
