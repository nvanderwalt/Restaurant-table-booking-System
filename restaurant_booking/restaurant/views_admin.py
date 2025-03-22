from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import timedelta, datetime

from django.conf import settings
from .models import Booking, Table, Menu, CustomUser
from .forms import TableForm, MenuForm, BookingForm

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, "You don't have permission to access the admin area.")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Dashboard
@login_required
@admin_required
def admin_dashboard(request):
    today = timezone.now().date()
    
    todays_bookings = Booking.objects.filter(date=today).order_by('time')
    
    today_bookings = todays_bookings.count()
    total_guests_today = sum(booking.number_of_guests for booking in todays_bookings)
    menu_items_count = Menu.objects.count()
    
    first_day_of_month = today.replace(day=1)
    new_customers_this_month = CustomUser.objects.filter(date_joined__gte=first_day_of_month).count()
    
    max_bookings_per_day = 50
    today_bookings_percent = min(int(today_bookings / max_bookings_per_day * 100), 100)
    
    max_guests_per_day = 200 
    guests_percent = min(int(total_guests_today / max_guests_per_day * 100), 100)
    
    max_new_customers = 100
    new_customers_percent = min(int(new_customers_this_month / max_new_customers * 100), 100)
    
    popular_tables = Table.objects.annotate(
        booking_count=Count('booking')
    ).order_by('-booking_count')[:5]
    
    week_dates = []
    week_data = []
    week_labels = []
    
    for i in range(7):
        date = today - timedelta(days=6-i)
        week_dates.append(date)
        count = Booking.objects.filter(date=date).count()
        week_data.append(count)
        week_labels.append(date.strftime('%a'))
    
    month_dates = []
    month_data = []
    month_labels = []
    
    for i in range(30):
        date = today - timedelta(days=29-i)
        month_dates.append(date)
        count = Booking.objects.filter(date=date).count()
        month_data.append(count)
        month_labels.append(date.strftime('%d %b'))
    
    recent_activities = [
        {
            'type': 'booking',
            'icon': 'calendar-check',
            'description': 'New reservation made by John Smith',
            'time': timezone.now() - timedelta(hours=2)
        },
        {
            'type': 'user',
            'icon': 'user-plus',
            'description': 'New customer registered: Mary Johnson',
            'time': timezone.now() - timedelta(hours=5)
        },
        {
            'type': 'menu',
            'icon': 'utensils',
            'description': 'Menu item updated: Grilled Salmon',
            'time': timezone.now() - timedelta(hours=8)
        },
        {
            'type': 'system',
            'icon': 'cog',
            'description': 'System backup completed successfully',
            'time': timezone.now() - timedelta(days=1)
        }
    ]
    
    context = {
        'today': today,
        'todays_bookings': todays_bookings[:5], 
        'today_bookings': today_bookings,
        'today_bookings_percent': today_bookings_percent,
        'total_guests_today': total_guests_today,
        'guests_percent': guests_percent,
        'menu_items_count': menu_items_count,
        'new_customers_this_month': new_customers_this_month,
        'new_customers_percent': new_customers_percent,
        'popular_tables': popular_tables,
        'recent_activities': recent_activities,
        'chart_labels': week_labels,
        'chart_data': week_data,
        'week_labels': week_labels,
        'week_data': week_data,
        'month_labels': month_labels,
        'month_data': month_data
    }
    
    return render(request, 'admin/dashboard.html', context)

# Bookings Management
@login_required
@admin_required
def admin_bookings(request):
    today = timezone.now().date()
    
    date_filter = request.GET.get('date')
    status_filter = request.GET.get('status')
    
    bookings = Booking.objects.all().order_by('-date', '-time')
    
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            bookings = bookings.filter(date=filter_date)
        except ValueError:
            messages.error(request, "Invalid date format")
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get('page')
    bookings_page = paginator.get_page(page_number)
    
    context = {
        'bookings': bookings_page,
        'today': today,
        'date_filter': date_filter,
        'status_filter': status_filter
    }
    
    return render(request, 'admin/booking_list.html', context)


# Booking Detail
@login_required
@admin_required
def admin_booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    today = timezone.now().date()
    
    other_bookings = Booking.objects.filter(user=booking.user).exclude(id=booking.id).order_by('-date')[:5]
    
    customer_booking_count = Booking.objects.filter(user=booking.user).count()
    customer_visits = Booking.objects.filter(user=booking.user, date__lt=today).count()
    
    user_bookings = Booking.objects.filter(user=booking.user)
    if user_bookings.exists():
        total_guests = sum(b.number_of_guests for b in user_bookings)
        avg_party_size = round(total_guests / user_bookings.count(), 1)
    else:
        avg_party_size = 0
    
    notes_history = []
    
    context = {
        'booking': booking,
        'today': today,
        'other_bookings': other_bookings,
        'customer_booking_count': customer_booking_count,
        'customer_visits': customer_visits,
        'avg_party_size': avg_party_size,
        'notes_history': notes_history
    }
    
    return render(request, 'admin/booking_detail.html', context)

# Add Booking
@login_required
@admin_required
def admin_booking_add(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            
            user_id = request.POST.get('user')
            if user_id:
                try:
                    user = CustomUser.objects.get(id=user_id)
                    booking.user = user
                    booking.save()
                    messages.success(request, "Booking created successfully")
                    return redirect('admin_booking_detail', booking_id=booking.id)
                except CustomUser.DoesNotExist:
                    form.add_error(None, "Selected user does not exist")
            else:
                form.add_error(None, "Please select a user for this booking")
    else:
        form = BookingForm()
        initial_user_id = request.GET.get('user')
        if initial_user_id:
            try:
                initial_user = CustomUser.objects.get(id=initial_user_id)
                form.initial['user'] = initial_user.id
            except CustomUser.DoesNotExist:
                pass
    
    users = CustomUser.objects.all().order_by('username')
    
    context = {
        'form': form,
        'users': users
    }
    
    return render(request, 'admin/booking_form.html', context)


# Edit Booking
@login_required
@admin_required
def admin_booking_edit(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully")
            return redirect('admin_booking_detail', booking_id=booking.id)
    else:
        form = BookingForm(instance=booking)
    
    context = {
        'form': form
    }
    
    return render(request, 'admin/booking_form.html', context)

# Confirm Booking
@login_required
@admin_required
def admin_booking_confirm(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status != 'CONFIRMED':
        booking.status = 'CONFIRMED'
        booking.save()
        messages.success(request, "Booking confirmed successfully")
    
    return redirect('admin_booking_detail', booking_id=booking.id)

# Cancel Booking
@login_required
@admin_required
def admin_booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if booking.status != 'CANCELLED':
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, "Booking cancelled successfully")
    
    return redirect('admin_booking_detail', booking_id=booking.id)

# Delete Booking
@login_required
@admin_required
def admin_booking_delete(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted successfully")
        return redirect('admin_bookings')
    
    context = {
        'booking': booking
    }
    
    return render(request, 'admin/booking_delete.html', context)

# Table Management
@login_required
@admin_required
def admin_tables(request):
    tables = Table.objects.all().order_by('number')
    
    context = {
        'tables': tables
    }
    
    return render(request, 'admin/table_management.html', context)

# Menu Management
@login_required
@admin_required
def admin_menu(request):
    menu_items = Menu.objects.all().order_by('category', 'name')
    
    context = {
        'menu_items': menu_items
    }
    
    return render(request, 'admin/menu.html', context)

# Add Menu Item
@login_required
@admin_required
def admin_menu_add(request):
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save()
            messages.success(request, "Menu item added successfully")
            return redirect('admin_menu')
    else:
        form = MenuForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'admin/menu_form.html', context)

# Edit Menu Item
@login_required
@admin_required
def admin_menu_edit(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    
    if request.method == 'POST':
        form = MenuForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            if request.POST.get('remove_image') == 'true' and menu_item.image:
                menu_item.image = None
            
            form.save()
            messages.success(request, "Menu item updated successfully")
            return redirect('admin_menu')
    else:
        form = MenuForm(instance=menu_item)
    
    context = {
        'form': form
    }
    
    return render(request, 'admin/menu_form.html', context)

# Toggle Menu Item Availability
@login_required
@admin_required
def admin_menu_toggle_availability(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    
    menu_item.is_available = not menu_item.is_available
    menu_item.save()
    
    status = "available" if menu_item.is_available else "unavailable"
    messages.success(request, f"Menu item marked as {status}")
    
    return redirect('admin_menu')

@login_required
@admin_required
def admin_booking_notes(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        admin_notes = request.POST.get('admin_notes', '')
        booking.admin_notes = admin_notes
        booking.save()
        
        messages.success(request, "Notes updated successfully")
    
    return redirect('admin_booking_detail', booking_id=booking.id)


# Table Administration Views
@login_required
@admin_required
def admin_table_add(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            table = form.save()
            messages.success(request, f"Table {table.number} created successfully")
            return redirect('admin_tables')
    else:
        form = TableForm()
    
    context = {
        'form': form,
        'title': 'Add New Table'
    }
    
    return render(request, 'admin/table_form.html', context)

@login_required
@admin_required
def admin_table_edit(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, f"Table {table.number} updated successfully")
            return redirect('admin_tables')
    else:
        form = TableForm(instance=table)
    
    context = {
        'form': form,
        'table': table,
        'title': f'Edit Table {table.number}'
    }
    
    return render(request, 'admin/table_form.html', context)

@login_required
@admin_required
def admin_table_delete(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    
    if request.method == 'POST':
        table_number = table.number
        
        bookings = Booking.objects.filter(table=table)
        if bookings.exists():
            messages.error(request, f"Cannot delete Table {table_number} because it has bookings")
            return redirect('admin_tables')
        
        table.delete()
        messages.success(request, f"Table {table_number} deleted successfully")
        return redirect('admin_tables')
    
    context = {
        'table': table,
        'bookings_count': Booking.objects.filter(table=table).count()
    }
    
    return render(request, 'admin/table_delete.html', context)

@login_required
@admin_required
def admin_table_detail(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    today = timezone.now().date()
    
    upcoming_bookings = Booking.objects.filter(
        table=table,
        date__gte=today
    ).order_by('date', 'time')[:10]
    
    total_bookings = Booking.objects.filter(table=table).count()
    bookings_this_month = Booking.objects.filter(
        table=table,
        date__month=today.month, 
        date__year=today.year
    ).count()
    
    days_in_month = 30  
    bookings_per_day = 8
    potential_bookings = days_in_month * bookings_per_day
    
    if potential_bookings > 0:
        utilization_rate = (bookings_this_month / potential_bookings) * 100
    else:
        utilization_rate = 0
    
    context = {
        'table': table,
        'upcoming_bookings': upcoming_bookings,
        'total_bookings': total_bookings,
        'bookings_this_month': bookings_this_month,
        'utilization_rate': round(utilization_rate, 1),
        'today': today
    }
    
    return render(request, 'admin/table_detail.html', context)

# Menu Administration Views
@login_required
@admin_required
def admin_menu_delete(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    
    if request.method == 'POST':
        item_name = menu_item.name
        menu_item.delete()
        messages.success(request, f"Menu item '{item_name}' deleted successfully")
        return redirect('admin_menu')
    
    context = {
        'menu_item': menu_item
    }
    
    return render(request, 'admin/menu_delete.html', context)

@login_required
@admin_required
def admin_menu_duplicate(request, menu_id):
    original_item = get_object_or_404(Menu, id=menu_id)
    
    new_item = Menu.objects.create(
        name=f"Copy of {original_item.name}",
        description=original_item.description,
        price=original_item.price,
        category=original_item.category,
        is_available=original_item.is_available
    )
    
    if original_item.image:
        from django.core.files.base import ContentFile
        from io import BytesIO
        from PIL import Image
        import os
        
        img = Image.open(original_item.image.path)
        
        img_io = BytesIO()
        img_format = os.path.splitext(original_item.image.name)[1][1:].upper()
        img.save(img_io, format=img_format)
        img_io.seek(0)
        
        new_item.image.save(
            f"copy_{original_item.image.name}",
            ContentFile(img_io.read()),
            save=True
        )
    
    messages.success(request, f"Menu item duplicated as '{new_item.name}'")
    return redirect('admin_menu_edit', menu_id=new_item.id)

# Customer Administration Views
@login_required
@admin_required
def admin_customers(request):
    search = request.GET.get('search', '')
    
    if search:
        customers = CustomUser.objects.filter(
            Q(username__icontains=search) | 
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        ).order_by('username')
    else:
        customers = CustomUser.objects.all().order_by('username')
    
    paginator = Paginator(customers, 20)  
    page_number = request.GET.get('page')
    customers_page = paginator.get_page(page_number)
    
    for customer in customers_page:
        customer.bookings_count = Booking.objects.filter(user=customer).count()
        customer.last_booking = Booking.objects.filter(user=customer).order_by('-date').first()
    
    context = {
        'customers': customers_page,
        'search': search
    }
    
    return render(request, 'admin/customers.html', context)

@login_required
@admin_required
def admin_customer_detail(request, user_id):
    customer = get_object_or_404(CustomUser, id=user_id)
    
    bookings = Booking.objects.filter(user=customer).order_by('-date')
    
    bookings_count = bookings.count()
    upcoming_bookings = bookings.filter(date__gte=timezone.now().date()).count()
    completed_bookings = bookings.filter(date__lt=timezone.now().date()).count()
    cancelled_bookings = bookings.filter(status='CANCELLED').count()
    
    if bookings.exists():
        from django.db.models import Count
        favorite_table = Table.objects.filter(
            booking__user=customer
        ).annotate(
            count=Count('id')
        ).order_by('-count').first()
    else:
        favorite_table = None
    
    if bookings.exists():
        avg_party_size = bookings.aggregate(avg=Avg('number_of_guests'))['avg']
        avg_party_size = round(avg_party_size, 1)
    else:
        avg_party_size = 0
    
    context = {
        'customer': customer,
        'bookings': bookings[:10],
        'bookings_count': bookings_count,
        'upcoming_bookings': upcoming_bookings,
        'completed_bookings': completed_bookings,
        'cancelled_bookings': cancelled_bookings,
        'favorite_table': favorite_table,
        'avg_party_size': avg_party_size,
        'member_since': customer.date_joined,
        'days_as_member': (timezone.now().date() - customer.date_joined.date()).days
    }
    
    return render(request, 'admin/customer_detail.html', context)

# Reports View
@login_required
@admin_required
def admin_reports(request):
    today = timezone.now().date()
    
    report_type = request.GET.get('type', 'bookings')
    period = request.GET.get('period', 'month')
    
    if period == 'week':
        start_date = today - timedelta(days=7)
        date_format = '%a'
    elif period == 'month':
        start_date = today - timedelta(days=30)
        date_format = '%d %b'
    elif period == 'year':
        start_date = today - timedelta(days=365)
        date_format = '%b' 
    else:  
        try:
            start_date = datetime.strptime(request.GET.get('start_date', ''), '%Y-%m-%d').date()
            end_date = datetime.strptime(request.GET.get('end_date', ''), '%Y-%m-%d').date()
            date_format = '%d %b'
        except ValueError:
            start_date = today - timedelta(days=30)
            end_date = today
            date_format = '%d %b'
    
    if period != 'custom':
        end_date = today
    
    if report_type == 'bookings':
        bookings_by_date = {}
        
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            bookings_by_date[current_date] = 0
            current_date += timedelta(days=1)
        
        bookings = Booking.objects.filter(date__gte=start_date, date__lte=end_date)
        for booking in bookings:
            if booking.date in bookings_by_date:
                bookings_by_date[booking.date] += 1
        
        labels = [date.strftime(date_format) for date in date_range]
        data = [bookings_by_date[date] for date in date_range]
        
        total_bookings = bookings.count()
        avg_bookings_per_day = total_bookings / len(date_range) if date_range else 0
        total_guests = sum(booking.number_of_guests for booking in bookings)
        avg_guests_per_booking = total_guests / total_bookings if total_bookings else 0
        
        status_counts = {
            'PENDING': bookings.filter(status='PENDING').count(),
            'CONFIRMED': bookings.filter(status='CONFIRMED').count(),
            'CANCELLED': bookings.filter(status='CANCELLED').count()
        }
        
        popular_hours = {}
        for booking in bookings:
            hour = booking.time.hour
            popular_hours[hour] = popular_hours.get(hour, 0) + 1
        
        popular_hours = dict(sorted(popular_hours.items(), key=lambda x: x[1], reverse=True)[:5])
        
        popular_hours_display = {}
        for hour, count in popular_hours.items():
            suffix = 'AM' if hour < 12 else 'PM'
            display_hour = hour % 12
            if display_hour == 0:
                display_hour = 12
            popular_hours_display[f"{display_hour} {suffix}"] = count
        
        context = {
            'report_type': report_type,
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'today': today,
            'chart_labels': labels,
            'chart_data': data,
            'total_bookings': total_bookings,
            'avg_bookings_per_day': round(avg_bookings_per_day, 1),
            'total_guests': total_guests,
            'avg_guests_per_booking': round(avg_guests_per_booking, 1),
            'status_counts': status_counts,
            'popular_hours': popular_hours_display
        }
    
    elif report_type == 'customers':
        new_customers_by_date = {}
        
        date_range = []
        current_date = start_date
        while current_date <= end_date:
            date_range.append(current_date)
            new_customers_by_date[current_date] = 0
            current_date += timedelta(days=1)
        
        customers = CustomUser.objects.filter(date_joined__date__gte=start_date, date_joined__date__lte=end_date)
        for customer in customers:
            join_date = customer.date_joined.date()
            if join_date in new_customers_by_date:
                new_customers_by_date[join_date] += 1
        
        labels = [date.strftime(date_format) for date in date_range]
        data = [new_customers_by_date[date] for date in date_range]
        
        total_customers = CustomUser.objects.count()
        new_customers = customers.count()
        
        active_customers = CustomUser.objects.filter(
            booking__date__gte=today - timedelta(days=30)
        ).distinct().count()
        
        top_customers = CustomUser.objects.annotate(
            booking_count=Count('booking')
        ).order_by('-booking_count')[:10]
        
        context = {
            'report_type': report_type,
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'today': today,
            'chart_labels': labels,
            'chart_data': data,
            'total_customers': total_customers,
            'new_customers': new_customers,
            'active_customers': active_customers,
            'top_customers': top_customers
        }
    
    return render(request, 'admin/reports.html', context)

# Settings View
@login_required
@admin_required
def admin_settings(request):
    if request.method == 'POST':
        messages.success(request, "Settings updated successfully")
        return redirect('admin_settings')
    
    import platform
    import django
    
    system_info = {
        'os': platform.system() + ' ' + platform.release(),
        'python_version': platform.python_version(),
        'django_version': django.__version__,
        'server_time': timezone.now(),
        'timezone': settings.TIME_ZONE,
        'debug_mode': settings.DEBUG
    }
    
    db_stats = {
        'total_users': CustomUser.objects.count(),
        'total_bookings': Booking.objects.count(),
        'total_tables': Table.objects.count(),
        'total_menu_items': Menu.objects.count()
    }
    
    context = {
        'system_info': system_info,
        'db_stats': db_stats
    }
    
    return render(request, 'admin/settings.html', context)