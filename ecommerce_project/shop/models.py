from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.urls import reverse

from django.core import serializers
from django.http import JsonResponse
import json


class Category(models.Model):
    """Model category"""
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        """In this class,
        we sort by name and correctly set the name in the admin panel"""
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_url(self):
        """This function from displays a page with products
         that are associated with a specific category,
         associated with the slug field."""
        return reverse('shop:products_by_category', args=[self.slug])

    def __str__(self):
        """Return a string representation of the name
        for in the admin panel"""
        return self.name


class Product(models.Model):
    """Product model"""
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product', blank=True)
    stock = models.IntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """In this class,
         we sort by name and correctly set the name in the admin panel"""
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Product'

    def get_url(self):
        """This function redirects the user to the product page
        associated with a particular category
        associated with the field category_slug and product_slug."""
        return reverse('shop:product_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        """Return a string representation of the name
        for in the admin panel"""
        return self.name

    def products_to_json(request):
        """A script that writes the model to product.json and serves to write
        the image field into a json-friendly one, since it is not possible to simply load the model into fixtures
        """
        products = Product.objects.all()

        products_list = []
        for product in products:
            products_list.append({
                "name": product.name,
                "slug": product.slug,
                "description": product.description,
                "category": product.category.name,
                "price": str(product.price),
                "image_url": product.image.url if product.image else None,
                "stock": product.stock,
                "available": product.available,
                "created": product.created.strftime('%Y-%m-%d %H:%M:%S'),
                "updated": product.updated.strftime('%Y-%m-%d %H:%M:%S'),
            })

        json_data = json.dumps(products_list, ensure_ascii=False)
        with open("fixtures/products.json", "w") as json_file:
            json.dump(json_data, json_file)


class Cart(models.Model):
    """Full cart"""
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        """In this class, we sort by name"""
        db_table = 'Cart'

    def __str__(self):
        """Return a string representation of the name
        for in the admin panel"""
        return self.cart_id


class CartItem(models.Model):
    """Information about one object-product added in cart"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sum_total(self):
        """Check out the entire cost of this item in the cart"""
        return self.product.price * self.quantity

    def __str__(self):
        """Return a string representation of the name
        for in the admin panel"""
        return self.product


class User(AbstractUser):
    image = models.ImageField(upload_to='users/', null=True, blank=True)

