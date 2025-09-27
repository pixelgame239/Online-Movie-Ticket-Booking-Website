from django.test import TestCase
from users.models import User
from django.db import IntegrityError
from django.urls import reverse

# Create your tests here.
class UserModelTest(TestCase):
    def test_user_registration(self):
        user = User.objects.create_user(username="testingaccount", password="password123", email="testing@gmail.com")
        self.assertEqual(user.username, 'testingaccount')
        self.assertTrue(user.check_password('password123'))
        self.assertEqual(user.email, "testing@gmail.com")
        self.assertFalse(user.is_superuser)
    def test_duplicate_username_fails(self):
        User.objects.create_user(username="testingaccount", password="password123", email="testing@gmail.com")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(username="testingaccount", password="password123", email="testing@gmail.com")
class ProfileUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testingaccount',
            password='password123',
            email='testing@gmail.com',
            phone= '123456789',
            address= '123 New Street',
            birth_date= '2000-01-01',
            gender = 'M',
        )
        self.client.login(username='testingaccount', password='password123')
        self.url = reverse('users:profile_edit')

    def test_profile_update_success_with_change(self):
        response = self.client.post(self.url, {
            'username': self.user.username,
            'phone': '012345678',
            'address': '123 Old Street',
            'email':'testing@gmail.com',
            'birth_date': '2002-09-02',
            'gender': 'F',
        })

        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '012345678')
        self.assertEqual(self.user.address, '123 Old Street')
        self.assertEqual(self.user.gender, 'F')
        self.assertEqual(response.status_code, 302)
    def test_profile_update_success_no_change(self):
        response = self.client.post(self.url, {
            'username': self.user.username,
            'phone': '123456789',
            'address': '123 New Street',
            'email':'testing@gmail.com',
            'birth_date': '2000-01-01',
            'gender': 'M',
        })

        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, '123456789')
        self.assertEqual(self.user.address, '123 New Street')
        self.assertEqual(self.user.gender, 'M')
        self.assertEqual(response.status_code, 302)
    def test_profile_update_fail(self):
        # Send incomplete POST (missing required fields like 'username' and 'email')
        response = self.client.post(self.url, {
            'phone': '012345678',
            'address': '123 Old Street',
        })
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertEqual(form.errors['email'], ['This field is required.'])


