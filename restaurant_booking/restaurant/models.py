from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.forms import ValidationError
from datetime import time

class CustomUser(AbstractUser):
    ADMIN = 'admin'
    STAFF = 'staff'
    CUSTOMER = 'customer'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (STAFF, 'Staff'),
        (CUSTOMER, 'Customer'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=CUSTOMER,
    )

    def __str__(self):
        return self.username
    
class Table(models.Model):
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    
    def __str__(self):
        return f"Table {self.number} (Seats {self.capacity})"

class Menu(models.Model):
    CATEGORY_CHOICES = [
        ('APPETIZER', 'Appetizer'),
        ('SOUP', 'Soup'),
        ('SALAD', 'Salad'),
        ('MAIN', 'Main Dish'),
        ('DESSERT', 'Dessert'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.URLField(max_length=200, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(default=time(12, 0))
    number_of_guests = models.IntegerField(default=1)
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Booking for {self.user.username} on {self.date} at {self.time}"
    
    def clean(self):
        conflicting_bookings = Booking.objects.filter(
            table=self.table,
            date=self.date,
            time=self.time,
            status__in=['PENDING', 'CONFIRMED']
        ).exclude(pk=self.pk)
        
        if conflicting_bookings.exists():
            raise ValidationError("This table is already booked for the selected time.")
        
        if self.number_of_guests > self.table.capacity:
            raise ValidationError("The number of guests exceeds the table capacity.")