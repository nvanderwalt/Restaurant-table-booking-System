from pyexpat.errors import messages
from django.forms import ValidationError
from django.shortcuts import redirect, render, get_object_or_404
from .models import Table, Menu, Booking
from django.http import HttpResponse
from .forms import BookingForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import logout, login, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                next_url = request.POST.get('next', '')
                
                if next_url:
                    return redirect(next_url)
                elif user.role == 'admin':
                    return redirect('admin_dashboard')
                else:
                    return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'restaurant/login.html', {
        'form': form,
        'next': request.GET.get('next', '')
    })

def index(request):
    return render(request, 'restaurant/index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'restaurant/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

def menu_view(request):
    menu_items = Menu.objects.filter(is_available=True).order_by('category')
    return render(request, 'restaurant/menu.html', {'menu_items': menu_items})

@login_required
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            
            try:
                booking.full_clean()
                booking.save()
                messages.success(request, "Your booking has been successfully created!")
                return redirect('booking_detail', booking_id=booking.id)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != '__all__' else None, error)
    else:
        form = BookingForm()
    
    tables = Table.objects.all()
    return render(request, 'restaurant/booking_form.html', {'form': form, 'tables': tables})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'restaurant/booking_detail.html', {'booking': booking})

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')
    return render(request, 'restaurant/booking_list.html', {'bookings': bookings})

@login_required
def booking_edit(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.date < timezone.now().date():
        messages.error(request, "Cannot edit past bookings.")
        return redirect('booking_list')
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Your booking has been updated!")
                return redirect('booking_detail', booking_id=booking.id)
            except ValidationError as e:
                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field if field != '__all__' else None, error)
    else:
        form = BookingForm(instance=booking)
    
    return render(request, 'restaurant/booking_edit.html', {'form': form, 'booking': booking})

@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.date < timezone.now().date():
        messages.error(request, "Cannot cancel past bookings.")
        return redirect('booking_list')
    
    if request.method == 'POST':
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, "Your booking has been cancelled.")
        return redirect('booking_list')
    
    return render(request, 'restaurant/booking_cancel.html', {'booking': booking})

def booking_confirmation_view(request):
    return HttpResponse("Booking Confirmed!")
