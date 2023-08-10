from .models import Category, Cart, CartItem
from .views import _cart_id
from django.core.exceptions import ObjectDoesNotExist


def menu_links(request):
    """For convenience, categories have been added to
     context_processors for access wherever they are needed."""
    links = Category.objects.all()
    return dict(links=links)


def counter(request):
    """We are trying to get the desired basket from the database, where it will be equal
    to the basket in the session, if there is, we take all the objects from there,
    and to count the number of all objects in the basket,
    if there are none, then the number is zero"""
    item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                item_count += cart_item.quantity
        except ObjectDoesNotExist:
            item_count = 0
    return dict(item_count=item_count)
