import json
import uuid
import random
import string

from django.shortcuts import redirect
from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse, reverse_lazy, resolve
from django.contrib.auth.models import AnonymousUser, User

from .forms import *
from .models import CustomUser, Product, Currency

#from .views import registration_view


class SimpleTest(TestCase):

    def setUp(self):
        #uname = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(10))
        self.plain_password = 'top_secret'
        self.user = CustomUser.objects.create_user(username='3PgtXSpw8P', email='dorlov@merann.ru', password=self.plain_password)
        self.user.confirmation_code = str(uuid.uuid4())
        self.user.save()
        self.c = Client()

    def test_a_register(self):
        new_username = self.user.username + '123'
        response = self.c.post(reverse_lazy("showcase:register"), { 'first_name': new_username,
            'last_name' : 'levinson', 'email' : self.user.email, 'password' : self.user.password 
        })

        self.assertEqual(response.status_code, 200)
        user = CustomUser.objects.get(username=new_username)
        self.assertEqual(user is not None and user.is_active, False)
        url = reverse_lazy("showcase:confirm", kwargs={ 'confirmation_code' : user.confirmation_code, 'username' : user.username })
        response = self.c.get(url)
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(username=new_username)
        self.assertTrue(user is not None and user.is_active)

    def test_b_profile(self):
        user = CustomUser.objects.get(username=self.user.username)
        url = reverse_lazy("showcase:profile", kwargs={ 'pk' : str(user.pk) })
        response = self.c.get(url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.username in response.content)
  
    def test_c_login(self):
        url = reverse_lazy("showcase:confirm", kwargs={ 'confirmation_code' : self.user.confirmation_code, 'username' : self.user.username })
        response = self.c.get(url)
        self.assertEqual(response.status_code, 302)
        response = self.c.post(reverse_lazy("showcase:login"), { 'username': self.user.username, 'password' : self.plain_password, })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith('/showcase/'))

    def test_d_logout(self):
        response = self.c.get(reverse_lazy("showcase:logout"), {})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith, '/showcase/login')


    def test_e_itemlist(self):
        response = self.c.get(reverse_lazy("showcase:products"), {})
        self.assertEqual(response.status_code, 302)

    def test_f_details(self):
        iname = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(10))
        currency = Currency.objects.create(name='test_currency', int_code=1, char_code='TMP')
        item = Product.objects.create(name=iname, description='test', currency=Currency.objects.get(pk=currency.pk))

        url = reverse_lazy("showcase:details", kwargs={ 'pk' : str(item.pk) })
        response = self.c.get(url, {})
        self.assertEqual(response.status_code, 302)

