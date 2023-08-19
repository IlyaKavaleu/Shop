from django.shortcuts import render
from django.views.generic.edit import CreateView


class OrderCreateView(CreateView):
    template_name = 'orders/order-create.html'
