# from http import HTTPStatus
#
# from django.contrib.auth.models import User, Group
# from django.test import TestCase
# from django.urls import reverse
# from .models import Category, Product, Cart, CartItem
#
# from django.utils.timezone import now
# from .forms import SignUpForm
# from datetime import timedelta
#
#
# class HomeViewTestCase(TestCase):
#     """A test that checks the correct display of the home page,
#      also correct status code and correct template"""
#
#     def test_home_view(self):
#         """Check correct status code and correct template"""
#         path = reverse('shop:home')
#         response = self.client.get(path)
#
#         self.assertEquals(response.status_code, HTTPStatus.OK)
#         self.assertTemplateUsed(response, 'shop/home.html')
#
#
# class CategoryListViewTestCase(TestCase):
#     """A test that checks the correct match of product pages from the selected category
#      with the same category with products from the fixture, also correct status code and correct template,
#      for truth for correct display, two answers are listed"""
#     fixtures = ['categories.json']
#
#     def setUp(self):
#         """General variables with help setUp"""
#         self.products = Product.objects.all()
#         self.category = Category.objects.first()
#
#     def test_list(self):
#         """Check correct status code and correct template compare the
#         categories from the answer and from the fixtures, for correctness, edit into a list"""
#         path = reverse('shop:home')
#         response = self.client.get(path)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'shop/home.html')
#
#         products_from_response = response.context['products']
#         products_from_fixture = Product.objects.filter(category=self.category)
#         self.assertEqual(list(products_from_response), list(products_from_fixture))
#
#     def test_list_with_category(self):
#         """All categories are taken from context_processors and compared with categories from fixtures"""
#         path = reverse('shop:home')
#         response = self.client.get(path)
#         categories_from_response = response.context['links']
#         categories_from_fixture = Category.objects.all()
#         self.assertEqual(list(categories_from_response), list(categories_from_fixture))
#
#
# class AboutViewTestCase(TestCase):
#     """A test that checks the correct display of the home page,
#      also correct status code and correct template"""
#
#     def test_about_view(self):
#         """Check correct status code and correct template"""
#         path = reverse('shop:contacts')
#         response = self.client.get(path)
#
#         self.assertEquals(response.status_code, HTTPStatus.OK)
#         self.assertTemplateUsed(response, 'shop/contacts.html')
#
#
# class UserSignUpViewTestCase(TestCase):
#     """Test for status code, correct template, user registration,
#      check for successful registration
#     """
#     def setUp(self):
#         self.group = Group.objects.create(name='User')
#         self.path = reverse('shop:signup')
#         self.data = {
#             'first_name': 'john',
#             'last_name': 'wayne',
#             'username': 'john',
#             'password1': 'John12345',
#             'password2': 'John12345',
#             'email': 'kavaleuilia@gmail.com',
#         }
#
#     def test_user_register_get(self):
#         """Check correct status code and correct template"""
#         response = self.client.get(self.path)
#         self.assertEqual(response.status_code, HTTPStatus.OK)
#         self.assertTemplateUsed(response, 'shop/signup.html')
#
#     def test_user_register_post_success(self):
#         """In this test, we take a user and check that he does not exist, then we try to register
#         him and redirect to the main page, at the end we check that the user has been created
#         """
#         username = self.data['username']
#         self.assertFalse(User.objects.filter(username=username).exists())
#
#         response = self.client.post(self.path, self.data)
#         self.assertEqual(response.status_code, HTTPStatus.FOUND)
#         self.assertRedirects(response, reverse('shop:home'))
#         self.assertTrue(User.objects.filter(username=username).exists())
#
#     # def test_user_register_post_error(self):
#     #     User.objects.create(username=self.data['username'])
#     #     response = self.client.post(self.path, self.data)
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertContains(response, 'A user with that username already exists.', html=True)
