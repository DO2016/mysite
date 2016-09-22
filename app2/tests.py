from django.test import TestCase

# Create your tests here.
import random
import string
from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.test import Client
from .models import CustomUser
import json


#from .views import registration_view

class SimpleTest(TestCase):

    def setUp(self):
        #uname = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(10))
        self.plain_password = 'top_secret'
        self.user = CustomUser.objects.create_user(username='3PgtXSpw8P', email='dorlov@merann.ru', password=self.plain_password)
        self.user.confirmation_code = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for x in range(33))
        self.user.save()


    def test_a_register(self):
        c = Client()
        new_username = self.user.username + '123'

        response = c.post('http://127.0.0.1:8080/app2/register', { 'first_name': new_username,
            'last_name' : 'levinson', 'email' : self.user.email, 'password' : self.user.password 
        })
        self.assertEqual(response.status_code, 200)
        user = CustomUser.objects.get(username=new_username)
        self.assertEqual(user is not None and user.is_active, False)

        # confirmation
        # 127.0.0.1:8080/app2/confirm/QGVkHLtpJoJeFNyJJeipB4U7G1CIl7b0c/TTT

        url = 'http://127.0.0.1:8080/app2/confirm/' + user.confirmation_code + '/' + user.username
        response = c.get(url)
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(username=new_username)
        self.assertTrue(user is not None and user.is_active)



    def test_b_profile(self):
        c = Client()
        user = User.objects.get(username=self.user.username)
        response = c.post('http://127.0.0.1:8080/app2/profile/{0}/'.format(str(user.id)), {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.username in response.content)


     
    def test_c_login(self):
        c = Client()
        url = 'http://127.0.0.1:8080/app2/confirm/' + self.user.confirmation_code + '/' + self.user.username
        response = c.get(url)
        self.assertEqual(response.status_code, 302)

        response = c.post('http://127.0.0.1:8080/app2/login', { 'username': self.user.username, 'password' : self.plain_password, })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith('/app2/'))



    def test_d_logout(self):
        c = Client()
        response = c.post('http://127.0.0.1:8080/app2/logout', {})
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/app2/login' in response['Location'])

