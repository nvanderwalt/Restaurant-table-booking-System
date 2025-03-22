from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from restaurant.models import Table, Menu, Booking
from django.utils import timezone


class BookingViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")
        self.table = Table.objects.create(number=1, capacity=4)
        self.menu_item = Menu.objects.create(
            name="Grilled Salmon",
            description="A delicious grilled salmon",
            price=15.99,
            category="MAIN",
            image="https://example.com/salmon.jpg",
            is_available=True
        )

    def test_booking_view(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('booking_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/booking_form.html')

    def test_create_booking(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('booking_view'), {
            'user': self.user.id,
            'table': self.table.id,
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'number_of_guests': 3
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful creation
        self.assertRedirects(response, reverse('booking_detail', args=[1]))  # Assuming booking ID is 1

    def test_booking_list_view(self):
        self.client.login(username="testuser", password="testpassword")
        Booking.objects.create(
            user=self.user,
            table=self.table,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=2,
            status='CONFIRMED'
        )
        response = self.client.get(reverse('booking_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/booking_list.html')
        self.assertContains(response, "Booking for testuser")

    def test_booking_edit_view(self):
        booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=2,
            status='PENDING'
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('booking_edit', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurant/booking_edit.html')

    def test_booking_cancel_view(self):
        booking = Booking.objects.create(
            user=self.user,
            table=self.table,
            date=timezone.now().date(),
            time=timezone.now().time(),
            number_of_guests=2,
            status='PENDING'
        )
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('booking_cancel', args=[booking.id]), data={'confirmation': 'yes'})
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'CANCELLED')
        self.assertRedirects(response, reverse('booking_list'))
