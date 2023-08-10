from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView

from . import models
from .models import Product, Category, Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout


def home(request, category_slug=None):
    """A function that displays the main page and offers to select a section
    and show products in this section, or select all products in the store,
    the function takes the category_slug argument and pulls the desired
    category from the category_slug database, then pulls out all the
    records associated with this category, or you can choose everything
    in the store to display
    """
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
    """The function takes 2 arguments categoty_slug and product_slug,
     the first one associates this product with the category by slug, the second one is the name of the slug
     of the product itself, we try to get it, in case of failure we throw an exception, and pass it to the context
    """
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    context = {'product': product}
    return render(request, 'shop/product.html', context)


def _cart_id(request):
    """The function tries to get a session to work with the current basket,
     if there is no session, we create it
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    """In the add cart function, we take the product_id argument,
    then we get this product from the database, then we try to get
    the desired cart from the Cart model, which is equal to the cart
    in the session, if we don’t find it, then we create it in the database
    and save the state.

    Next, we try to get objects from the CartItem model, if this product was previously added,
    we increment it by 1, if it was not created with a value of 1, since this is the first product in this model.
    In both cases, save the state. And redirect to func cart_detail which performs a mathematical operation in the basket (see below).
    """
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except ObjectDoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except ObjectDoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    return redirect('shop:cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None):
    """The function accepting default arguments for future work with them,
    we try to get the already created basket from the database equal to the
    current basket in the session and pull out all the objects associated
    with the current basket. Next, we get the sum of all the items in the
    basket and the number of products. Throw an exception if it fails."""
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    context = {'cart_items': cart_items, 'total': total, 'counter': counter}
    return render(request, 'shop/cart.html', context)


def cart_remove(request, product_id):
    """A function that increments (deletes) a product from the basket,
    if the number of objects is 0, then the basket object itself
    is deleted"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('shop:cart_detail')


def remove_all_stock_from_cart(request, product_id):
    """Function to remove all products from the cart object"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(product=product_id, cart=cart)
    cart_items.delete()
    return redirect('shop:cart_detail')


def cart_remove_all(request):
    """A function that deletes all objects in the basket (empty basket)"""
    cart = Cart.objects.get(cart_id=_cart_id(request))
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items.delete()
    return redirect('shop:cart_detail')


def signupView(request):
    """A function that registers a user based on the
     SignUp form and the User model with a redirect to the main page,
     in case of failure, we get an empty form for retrying"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='User')
            user_group.user_set.add(signup_user)
            login(request, signup_user)
            return redirect('shop:home')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'shop/signup.html', context)


def loginView(request):
    """Authorization function with checking if this user exists using the
    authenticate function, if successful, redirect to the main page,
     if unsuccessful, try again"""
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('shop:home')
        else:
            return redirect('shop:signup')
    else:
        form = AuthenticationForm()
    context = {'form': form}
    return render(request, 'shop/login.html', context)


def logoutView(request):
    """The function to log out of your account"""
    logout(request)
    return redirect('shop:home')


def search(request):
    """The function by which the site is searched,
    an object from the form is accepted, then it checks whether
    this object is included in the name or description field,
    if it is, it returns all records from the database that this
    object is included in, if not, queryset returns none,
    for convenience search system implemented on the main page"""
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.none()

    context = {
        'query': query,
        'products': products,
    }
    return render(request, 'shop/home.html', context)


def contacts(request):
    context = {'contacts': 'Our Contact'}
    return render(request, 'shop/contacts.html', context)