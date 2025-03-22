# SpicyFood Restaurant Booking System

## Project Overview

SpicyFood Restaurant Booking System is a full-stack Django web application designed to streamline the restaurant booking process. The system allows customers to view the restaurant menu, make table reservations, and manage their bookings. It also provides an administrative interface for restaurant staff to manage bookings, tables, menu items, and view analytics.

### Key Features

- **Customer Features**
  - Browse restaurant menu by category
  - Make table reservations with date, time, and party size selection
  - Manage and view booking history
  - User registration and authentication

- **Admin Features**
  - Dashboard with key statistics and upcoming bookings
  - Comprehensive booking management
  - Table management with visual floor plan
  - Menu management
  - Customer management
  - Detailed analytics and reports
  - System settings and configuration

## Technology Stack

- **Backend**: Python 3.13, Django 5.1.7
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: PostgreSQL
- **Additional Libraries**: Font Awesome, Chart.js
- **Authentication**: Django's built-in authentication system

## Data Models

### Table
Represents dining tables in the restaurant.
- `number` (IntegerField): Unique table number
- `capacity` (IntegerField): Maximum number of guests the table can accommodate

### Menu
Represents menu items available at the restaurant.
- `name` (CharField): Name of the menu item
- `description` (TextField): Description of the menu item
- `price` (DecimalField): Price of the menu item
- `category` (CharField): Category of the menu item (Appetizer, Soup, Salad, Main Dish, Dessert)
- `image` (URLField): Image URL of the menu item
- `is_available` (BooleanField): Indicates if the item is currently available

### Booking
Represents customer bookings.
- `user` (ForeignKey to User): Customer who made the booking
- `table` (ForeignKey to Table): Reserved table
- `date` (DateField): Date of the reservation
- `time` (TimeField): Time of the reservation
- `number_of_guests` (IntegerField): Number of guests
- `special_requests` (TextField): Any special requests from the customer
- `status` (CharField): Status of the booking (Pending, Confirmed, Cancelled)
- `created_at` (DateTimeField): When the booking was created
- `admin_notes` (TextField): Notes from admin (not visible to customers)

### CustomUser
Represents the system's users (customers, staff, and admin).
- `username` (CharField): Username for login
- `email` (EmailField): Email address
- `role` (CharField): Role of the user (Admin, Staff, Customer)
- `date_joined` (DateTimeField): Date when the user account was created

## Setup and Installation

### Prerequisites
- Python 3.13 or higher
- PostgreSQL
- pip (Python package manager)

### Installation Steps

1. Clone the repository
   ```
   git clone https://github.com/nvanderwalt/Restaurant-table-booking-System.git

   cd restaurant-booking
   ```

2. Create and activate a virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Configure database in settings.py
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'restaurant_db',
           'USER': 'postgres',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. Run migrations
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser
   ```
   python manage.py createsuperuser
   ```

7. Run the development server
   ```
   python manage.py runserver
   ```

8. Access the application at http://localhost:8000/

## User Guide

### Customer Interface

#### Homepage
The homepage welcomes visitors with beautiful visuals of the restaurant's ambiance and cuisine. Users can navigate to the menu, make a reservation, or log in to manage their bookings.

#### Menu Page
The menu page displays all available dishes categorized by type (Appetizers, Soups, Salads, Main Dishes, Desserts). Users can filter the menu by category.

#### Booking Process
1. Navigate to the booking page
2. Select date, time, and number of guests
3. Choose an available table
4. Add any special requests
5. Confirm the booking
6. Receive a confirmation with booking details

#### My Bookings
Logged-in users can view their booking history, check the status of upcoming reservations, and cancel or modify bookings if needed.

### Admin Interface

#### Dashboard
The dashboard provides an overview of the restaurant's operations, including:
- Today's bookings count
- Total number of guests expected today
- Recent activity
- Popular tables
- Booking trends (weekly/monthly charts)

#### Bookings Management
Admins can:
- View all bookings with filtering options
- Add new bookings
- Edit booking details
- Confirm or cancel bookings
- Add internal notes to bookings

#### Table Management
The table management interface allows admins to:
- View the restaurant floor plan
- Add, edit, or remove tables
- View table utilization statistics
- See upcoming bookings for each table

#### Menu Management
The menu management interface allows admins to:
- Add new menu items with images (via URL)
- Edit existing menu items
- Toggle item availability
- Categorize items
- Duplicate popular items

#### Customer Management
Admins can:
- View customer information
- See booking history for each customer
- Track customer metrics (bookings, average party size)
- Identify frequent customers

#### Reports
The reporting interface provides analytics on:
- Booking trends over time
- Table utilization rates
- Customer growth
- Popular booking times

#### Settings
The settings page allows configuration of:
- Restaurant information
- Operating hours
- Booking intervals
- Maximum party size
- Advance booking period

## Security Implementation

### Authentication
- Django's built-in authentication system is used for user management
- Custom login and registration forms with validation
- Password hashing and security
- Session management

### Authorization
- Role-based access control
- Staff-only access to admin features
- Booking ownership validation
- CSRF protection

### Data Protection
- Form validation to prevent invalid data
- Double booking prevention
- SQL injection protection via Django's ORM
- XSS protection

## Testing

### Manual Testing
Manual testing was performed on:
- Responsive design across different devices
- Booking process
- User authentication
- Admin features
- Form validations
- Error handling

### Automated Testing
- Unit tests for models and views
- Integration tests for booking flow
- Form validation tests
- Security tests

## Future Enhancements

1. **Email Notifications**
   - Booking confirmations
   - Reminder emails
   - Marketing communications

2. **Online Payments**
   - Integration with payment gateways
   - Deposit requirements for large bookings
   - Gift cards

3. **Mobile App**
   - Native mobile applications for iOS and Android
   - Push notifications

4. **Waitlist Management**
   - Queue system for fully booked times
   - SMS notifications when tables become available

5. **Customer Feedback System**
   - Post-dining surveys
   - Rating system
   - Feedback management

6. **Advanced Analytics**
   - Revenue forecasting
   - Customer segmentation
   - Booking pattern analysis

## Conclusion

The SpicyFood Restaurant Booking System provides a comprehensive solution for managing restaurant reservations. The dual-interface design caters to both customers and staff, streamlining the booking process and providing valuable insights for business operations.

---