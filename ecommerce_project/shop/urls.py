from . import views
from django.urls import path

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>', views.home, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product, name='product_detail'),
    path('product/', views.product, name='product'),
    path('cart/', views.cart, name='cart')
]
