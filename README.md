# Rent-A-Car Management System

A comprehensive car rental management system built with Python and Tkinter, featuring user authentication, vehicle management, and rental operations.

## Features

### User Management
- **Registration**: New users can create accounts with email, username, and password
- **Authentication**: Secure login/logout functionality with session management
- **Profile Management**: Password change and account deletion capabilities
- **Auto-login**: Remembers logged-in users for convenience

### Vehicle Management
- **Vehicle Inventory**: Add, remove, and view cars with detailed information
- **Vehicle Details**: Brand, model, license plate, and daily pricing
- **Search & Filter**: Find vehicles by brand, model, or availability
- **Shopping Cart**: Add vehicles to rental cart for batch operations

### Rental Operations
- **Booking System**: Rent cars for specific date ranges
- **Availability Check**: Prevent double bookings with conflict detection
- **Return Management**: Track and update vehicle return dates
- **History Tracking**: Complete rental history and activity logs

## MVC Architecture

This project follows the **Model-View-Controller (MVC)** architectural pattern:

### Model Layer (`models/`)
- **auth.py**: Handles user data, authentication logic, and user-related operations
- **cars.py**: Manages vehicle data, rental operations, and business logic
- Encapsulates data access and business rules
- Interacts with CSV files for data persistence

### View Layer (`views/`)
- **auth.py**: Login/registration GUI interface
- **cars.py**: Main application interface for vehicle management
- Handles user interface components and user interactions
- Built with Tkinter for desktop GUI

### Controller Layer (`manage.py`)
- **manage.py**: Main application controller
- Coordinates between models and views
- Handles application flow and auto-login logic
- Manages user sessions and navigation

### Additional Components
- **methods/**: Utility functions and helpers
- **database/**: Data storage layer (CSV files)

## Project Structure

```
rent-a-car/
├── manage.py              # Controller - Main application entry point
├── models/                # Model - Data models and business logic
│   ├── auth.py           # User authentication and management
│   └── cars.py           # Vehicle and rental operations
├── views/                 # View - GUI components
│   ├── auth.py           # Login/registration interface
│   └── cars.py           # Main application interface
├── methods/               # Utility functions
│   ├── date.py           # Date/time operations
│   └── mail.py           # Email functionality
├── database/              # Data storage (CSV files)
│   ├── auth.csv          # User accounts
│   ├── cars.csv          # Vehicle inventory
│   ├── logs.csv          # Rental records
│   ├── history.csv       # Activity history
│   └── sepet.csv         # Shopping cart data
└── README.md             # This file
```

## Technology Stack

- **Backend**: Python 3.x
- **Architecture**: Model-View-Controller (MVC) pattern
- **GUI**: Tkinter
- **Database**: CSV files (pandas for data manipulation)
- **Data Processing**: pandas, random

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rent-a-car
```

2. Install required dependencies:
```bash
pip install pandas
```

3. Run the application:
```bash
python manage.py
```

## Usage

### First Time Setup
1. Run `manage.py` to start the application
2. Click "Sign Up" to create a new account
3. Enter your email, username, and password
4. Log in with your credentials

### Vehicle Management
1. Browse available vehicles in the main interface
2. Add vehicles to your cart for rental consideration
3. View detailed vehicle information including pricing
4. Filter vehicles by brand or model

### Rental Process
1. Select vehicles and add them to your cart
2. Choose rental dates (start and end dates)
3. Confirm rental - system checks for availability
4. Track rental status and return dates

### Admin Features
- Add new vehicles to the fleet
- Remove vehicles from inventory
- View complete rental history
- Monitor user activity

## Data Storage

The system uses CSV files for data persistence:
- **auth.csv**: User accounts and login status
- **cars.csv**: Vehicle fleet information
- **logs.csv**: Active rental records
- **history.csv**: Complete activity log
- **sepet.csv**: User shopping carts

## Security Features

- Password-based authentication
- Session management with auto-login
- Input validation for user registration
- Conflict prevention for rental bookings

## Sample Data

The system comes pre-loaded with sample vehicles:
- Toyota Corolla - 750 TL/day
- Honda Civic - 820 TL/day
- Ford Focus - 680 TL/day
- Volkswagen Golf - 900 TL/day
- Renault Megane - 700 TL/day

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions, please open an issue on the GitHub repository or contact the development team.

---

**Note**: This is a desktop application using Tkinter for the GUI. Ensure you have Python installed with the tkinter library (usually included with Python installations).
