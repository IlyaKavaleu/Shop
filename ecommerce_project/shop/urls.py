from . import views
from django.urls import path
from django.views.decorators.cache import cache_page


app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>', views.home, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product, name='product_detail'),
    path('product/', cache_page(10)(views.product), name='product'),

    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>', views.cart_remove, name='cart_remove'),
    path('cart/cart_remove_all_stock_from_cart/<int:product_id>', cache_page(10)(views.remove_all_stock_from_cart), name='remove_all_stock_from_cart'),
    path('cart/remove_all/', views.cart_remove_all, name='cart_remove_all'),
    path('account/create/', views.signupView, name='signup'),
    path('account/login/', views.loginView, name='login'),
    path('account/logout/', views.logoutView, name='logout'),
    path('search/', cache_page(10)(views.search), name='search'),
    path('contacts/', views.contacts, name='contacts'),
    path('about/', views.about, name='about'),
    path('cabinet/', views.cabinet, name='cabinet'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password')
]
