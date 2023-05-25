from django.test import TestCase

from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import SocialAccount
from user_choices import InterestingChoices
from .models import User


# user_test
class UserModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            phone='123456789',
            age=25,
            address='Test Address',
            interesting=InterestingChoices.PERSONAL
        )

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.phone, '123456789')
        self.assertEqual(user.age, 25)
        self.assertEqual(user.address, 'Test Address')
        self.assertEqual(user.interesting, 'Art')


# social_account_test
class SocialAccountAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.account_data = {
            'user': self.user.id,
            'social_account': 'google'
        }
        self.url = reverse('social-account-list')

    def test_create_social_account(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, self.account_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SocialAccount.objects.count(), 1)
        self.assertEqual(SocialAccount.objects.get().social_account, 'google')
