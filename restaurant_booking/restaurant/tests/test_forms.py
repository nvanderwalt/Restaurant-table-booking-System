from django.test import TestCase
from django import forms
from django.contrib.auth import get_user_model
from restaurant.forms import BookingForm, UserRegistrationForm, MenuForm
from restaurant.models import Table, Menu

class BookingFormTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.table = Table.objects.create(number=1, capacity=4)

    def test_booking_form_valid(self):
        form_data = {
            'user': self.user.id,
            'table': self.table.id,
            'date': '2025-03-22',
            'time': '12:00:00',
            'number_of_guests': 3
        }
        form = BookingForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_booking_form_invalid(self):
        form_data = {
            'user': self.user.id,
            'table': self.table.id,
            'date': '2025-03-22',
            'time': '12:00:00',
            'number_of_guests': 10 
        }
        form = BookingForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('The number of guests exceeds the table capacity.', form.errors['number_of_guests'])

class UserRegistrationFormTest(TestCase):
    def test_user_registration_form_valid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password123',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_registration_form_invalid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'password123',
            'password2': 'password124', 
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())

class MenuFormTest(TestCase):
    def test_menu_form_valid(self):
        form_data = {
            'name': 'Grilled Salmon',
            'description': 'Delicious grilled salmon with herbs',
            'price': '19.99',
            'category': 'MAIN',
            'image': 'https://example.com/salmon.jpg',
            'is_available': True
        }
        form = MenuForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_menu_form_invalid(self):
        form_data = {
            'name': '',  
            'description': 'Delicious grilled salmon with herbs',
            'price': '19.99',
            'category': 'MAIN',
            'image': 'https://example.com/salmon.jpg',
            'is_available': True
        }
        form = MenuForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['This field is required.'])
