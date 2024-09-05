from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.authtoken.models import Token

class RegisterTestCase(APITestCase):
    
    
    def test_register(self):
        data = {
            "username": "testcase",
            "email": "test@mail.com",
            "password": "pass123",
            "password2": "pass123"
        }
        response=self.client.post(reverse('register-user'),data)
        # print(response.status_code==status.HTTP_201_CREATED)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        
        
class LoginLogoutTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(username='example',password='pass12345')
        
    def test_login(self):
        data = {
            "username": "example",
            "password": "pass12345"
        }
        response=self.client.post(reverse('login-user'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)