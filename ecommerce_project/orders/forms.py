from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    """Form for create order"""
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'name'}))
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'lastname'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'email'}))
    address = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'address'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address')
