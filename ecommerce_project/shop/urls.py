from . import views
from django.urls import path

app_name = 'shop'

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>', views.home, name='products_by_category'),
    path('product/', views.product, name='product')
]
