from django import forms
from .models import Booking, Table, Menu, CustomUser
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime, timedelta

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = CustomUser.ADMIN
        if commit:
            user.save()
        return user
        

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model = Booking
        fields = ['table', 'date', 'time', 'number_of_guests', 'special_requests']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%d')

class AdminBookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    
    class Meta:
        model = Booking
        fields = ['user', 'table', 'date', 'time', 'number_of_guests', 'special_requests', 'status']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs['min'] = datetime.now().strftime('%Y-%m-%d')
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        if 'user' in self.fields:
            self.fields['user'].widget.attrs.update({'class': 'form-control select2'})
        if 'table' in self.fields:
            self.fields['table'].widget.attrs.update({'class': 'form-control select2'})

class TableForm(forms.ModelForm):
    class Meta:
        model = Table
        fields = ['number', 'capacity']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
    def clean_number(self):
        number = self.cleaned_data.get('number')
        existing = Table.objects.filter(number=number)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        
        if existing.exists():
            raise forms.ValidationError("A table with this number already exists.")
        return number

class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['name', 'description', 'price', 'category', 'image', 'is_available']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'is_available':
                field.widget.attrs['class'] = 'form-control'
                
        if 'price' in self.fields:
            self.fields['price'].widget.attrs.update({
                'min': '0.01', 
                'step': '0.01'
            })