from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from restaurant.models import Table, Menu, Booking
from django.utils import timezone
from datetime import timedelta


class CustomUserModelTest(TestCase):
    def test_create_user(self):
        user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("testpassword"))

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(username="admin", password="adminpassword")
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class TableModelTest(TestCase):
    def test_table_creation(self):
        table = Table.objects.create(number=1, capacity=4)
        self.assertEqual(table.number, 1)
        self.assertEqual(table.capacity, 4)

    def test_str_method(self):
        table = Table.objects.create(number=2, capacity=6)
        self.assertEqual(str(table), "Table 2 (Seats 6)")


class MenuModelTest(TestCase):
    def test_menu_item_creation(self):
        menu_item = Menu.objects.create(
            name="Grilled Salmon",
            description="A delicious grilled salmon",
            price=15.99,
            category="MAIN",
            image="https://example.com/salmon.jpg",
            is_available=True
        )
        self.assertEqual(menu_item.name, "Grilled Salmon")
        self.assertEqual(menu_item.price, 15.99)
        self.assertEqual(menu_item.category, "MAIN")
        self.assertTrue(menu_item.is_available)

    def test_menu_item_str_method(self):
        menu_item = Menu.objects.create(
            name="Grilled Salmon",
            description="A delicious grilled salmon",
            price=15.99,
            category="MAIN",
            image="https://example.com/salmon.jpg",
            is_available=True
        )
        self.assertEqual(str(menu_item), "Grilled Salmon")


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.table = Table.objects.create(number=1, capacity=4)

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=3,
            status='PENDING'
        )
        self.assertEqual(booking.user.username, "testuser")
        self.assertEqual(booking.table.number, 1)
        self.assertEqual(booking.number_of_guests, 3)
        self.assertEqual(booking.status, 'PENDING')

    def test_booking_clean_method(self):
        booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=3,
            status='PENDING'
        )
        conflicting_booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=3,
            status='PENDING'
        )

        with self.assertRaises(ValidationError):
            booking.clean() 


class MenuItemImageTest(TestCase):
    def test_image_url_field(self):
        menu_item = Menu.objects.create(
            name="Pizza",
            description="Delicious cheese pizza",
            price=10.00,
            category="MAIN",
            image="https://example.com/pizza.jpg",
            is_available=True
        )
        self.assertEqual(menu_item.image, "https://example.com/pizza.jpg")
