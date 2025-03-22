from django.contrib import admin
from .models import Table, Menu, Booking

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity')
    list_filter = ('capacity',)
    search_fields = ('number',)

@admin.register(Menu)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'table', 'date', 'time', 'number_of_guests', 'status')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'special_requests')
    date_hierarchy = 'date'