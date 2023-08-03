from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Product, Category


def home(request, category_slug=None):
    category_page = None
    products = None
    if category_slug is not None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category_page, available=True)
    else:
        products = Product.objects.all().filter(available=True)

    context = {'products': products, 'category': category_page}
    return render(request, 'shop/home.html', context)


def product(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {'product': product}
    return render(request, 'shop/product.html', context)


def cart(request):
    return render(request, 'shop/cart.html')
