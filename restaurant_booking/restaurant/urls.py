from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin

from . import views_admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu_view, name='menu'),
    path('booking/', views.booking_view, name='booking'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('booking/<int:booking_id>/edit/', views.booking_edit, name='booking_edit'),
    path('booking/<int:booking_id>/cancel/', views.booking_cancel, name='booking_cancel'),
    path('mybookings/', views.booking_list, name='booking_list'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),


    # Admin URLs
    # path('admin/', admin.site.urls),
    path('admin-dashboard/', views_admin.admin_dashboard, name='admin_dashboard'),
    
    # Admin Booking URLs
    path('admin-bookings/', views_admin.admin_bookings, name='admin_bookings'),
    path('admin-booking/<int:booking_id>/', views_admin.admin_booking_detail, name='admin_booking_detail'),
    path('admin-booking-add/', views_admin.admin_booking_add, name='admin_booking_add'),
    path('admin-booking/<int:booking_id>/edit/', views_admin.admin_booking_edit, name='admin_booking_edit'),
    path('admin-booking/<int:booking_id>/confirm/', views_admin.admin_booking_confirm, name='admin_booking_confirm'),
    path('admin-booking/<int:booking_id>/cancel/', views_admin.admin_booking_cancel, name='admin_booking_cancel'),
    path('admin-booking/<int:booking_id>/delete/', views_admin.admin_booking_delete, name='admin_booking_delete'),
    path('admin-booking/<int:booking_id>/notes/', views_admin.admin_booking_notes, name='admin_booking_notes'),
    
    # Admin Table URLs
    path('admin-tables/', views_admin.admin_tables, name='admin_tables'),
    path('admin-table/add/', views_admin.admin_table_add, name='admin_table_add'),
    path('admin-table/<int:table_id>/edit/', views_admin.admin_table_edit, name='admin_table_edit'),
    path('admin-table/<int:table_id>/delete/', views_admin.admin_table_delete, name='admin_table_delete'),
    path('admin-table/<int:table_id>/', views_admin.admin_table_detail, name='admin_table_detail'),
    
    # Admin Menu URLs
    path('admin-menu/', views_admin.admin_menu, name='admin_menu'),
    path('admin-menu/add/', views_admin.admin_menu_add, name='admin_menu_add'),
    path('admin-menu/<int:menu_id>/edit/', views_admin.admin_menu_edit, name='admin_menu_edit'),
    path('admin-menu/<int:menu_id>/delete/', views_admin.admin_menu_delete, name='admin_menu_delete'),
    path('admin-menu/<int:menu_id>/toggle/', views_admin.admin_menu_toggle_availability, name='admin_menu_toggle_availability'),
    path('admin-menu/<int:menu_id>/duplicate/', views_admin.admin_menu_duplicate, name='admin_menu_duplicate'),
    
    # Admin Customer URLs
    path('admin-customers/', views_admin.admin_customers, name='admin_customers'),
    path('admin-customer/<int:user_id>/', views_admin.admin_customer_detail, name='admin_customer_detail'),
    
    # Admin Reports
    path('admin-reports/', views_admin.admin_reports, name='admin_reports'),
    
    # Admin Settings
    path('admin-settings/', views_admin.admin_settings, name='admin_settings'),
]