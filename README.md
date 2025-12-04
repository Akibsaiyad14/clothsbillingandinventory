# Cloth Shop Management System

A complete cloth shop billing and inventory management system with Django REST Framework backend and a beautiful, responsive frontend with smooth color gradients.

## Features

### Backend (Django DRF)
- **Inventory Management**: Manage cloth items (shirts, pants, t-shirts, etc.) with categories, sizes, colors, and pricing
- **Stock Management**: Track stock levels with low-stock alerts and automatic stock updates
- **Billing System**: Create bills with multiple items, apply discounts and taxes
- **PDF Generation**: Automatically generate professional PDF invoices using ReportLab (in Indian Rupees ₹)
- **RESTful API**: Complete REST API for all operations with filtering and search capabilities
- **JWT Authentication**: Secure token-based authentication system with refresh tokens

### Frontend
- **Dashboard**: Overview with statistics, low stock alerts, and recent bills
- **Inventory Page**: Add, edit, delete items; update stock levels; filter by category and size
- **Billing Page**: Create bills with item search, cart management, and automatic calculations
- **Reports Page**: View all bills with filtering options and detailed bill views
- **Login System**: Secure JWT-based authentication with username display and logout
- **Smooth Design**: Beautiful gradient color scheme with fully responsive mobile design
- **Mobile-Friendly**: Collapsible navigation menu and optimized layouts for small screens

## Tech Stack

### Backend
- Python 3.8+
- Django 4.2.7
- Django REST Framework 3.14.0
- Django REST Framework Simple JWT 5.3.0
- ReportLab 4.0.7 (PDF generation)
- SQLite (default database)

### Frontend
- HTML5
- CSS3 (with gradients and animations)
- Vanilla JavaScript (ES6+)
- Font Awesome icons
- JWT token storage via LocalStorage

## Installation & Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Create virtual environment:**
   ```powershell
   python -m venv venv
   ```

3. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run migrations:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser (optional):**
   ```powershell
   python manage.py createsuperuser
   ```

7. **Create demo user for testing:**
   ```powershell
   python manage.py create_demo_user
   ```
   This creates a demo user with credentials: `demo` / `demo1234`

8. **Run the development server:**
   ```powershell
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`

### Authentication & Login

**Demo User Credentials:**
- Username: `demo`
- Password: `demo1234`

**How to Login:**
1. Go to `http://localhost:8080/login.html`
2. Enter username and password
3. Click "Sign In"
4. You'll be redirected to the dashboard with your username displayed in the header

**JWT Token Authentication:**
- The system uses JWT (JSON Web Tokens) for secure authentication
- Access tokens are valid for 5 hours
- Refresh tokens are valid for 1 day
- Tokens are automatically refreshed when expired
- Creating bills requires authentication

**API Endpoints:**
- `POST /api/auth/login/` - Login (returns JWT tokens)
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/whoami/` - Get current user info (requires authentication)
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/token/refresh/` - Refresh access token

### Frontend Setup

1. **Navigate to frontend directory:**
   ```powershell
   cd frontend
   ```

2. **Open `index.html` in your browser:**
   - You can use any web server (Python's http.server, Live Server extension in VS Code, etc.)
   - Or simply open `index.html` directly in your browser

3. **Using Python's built-in server (recommended):**
   ```powershell
   python -m http.server 8080
   ```
   Then open `http://localhost:8080` in your browser

## Project Structure

```
clothShops/
├── backend/
│   ├── clothshop/          # Main project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── inventory/          # Inventory app
│   │   ├── models.py       # ClothItem, Stock models
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── billing/            # Billing app
│   │   ├── models.py       # Bill, BillItem models
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── pdf_generator.py
│   ├── manage.py
│   └── requirements.txt
└── frontend/
    ├── css/
    │   └── style.css       # All styles with gradients
    ├── js/
    │   ├── config.js       # API configuration
    │   ├── dashboard.js
    │   ├── inventory.js
    │   ├── billing.js
    │   └── reports.js
    ├── index.html          # Dashboard page
    ├── inventory.html      # Inventory management
    ├── billing.html        # Create bills
    └── reports.html        # View all bills
```

## API Endpoints

### Inventory
- `GET /api/inventory/items/` - List all items
- `POST /api/inventory/items/` - Create new item
- `GET /api/inventory/items/{id}/` - Get item details
- `PUT /api/inventory/items/{id}/` - Update item
- `DELETE /api/inventory/items/{id}/` - Delete item
- `GET /api/inventory/items/low_stock/` - Get low stock items
- `POST /api/inventory/stock/update_stock/` - Update stock quantity

### Billing
- `GET /api/billing/bills/` - List all bills
- `POST /api/billing/bills/` - Create new bill
- `GET /api/billing/bills/{id}/` - Get bill details
- `GET /api/billing/bills/{id}/download_pdf/` - Download bill PDF

## Usage

### Adding Items
1. Go to Inventory page
2. Click "Add New Item"
3. Fill in item details (name, category, size, color, price, SKU)
4. Set initial stock quantity
5. Click "Add Item"

### Managing Stock
1. Go to Inventory page
2. Find the item you want to update
3. Click "Update Stock"
4. Enter new stock quantity
5. Click "Update Stock"

### Creating Bills
1. Go to Billing page
2. Enter customer information
3. Search for items and add them to cart
4. Adjust quantities as needed
5. Set discount and tax rate (optional)
6. Add notes (optional)
7. Click "Create Bill"
8. PDF will automatically download

### Viewing Reports
1. Go to Reports page
2. Use filters to search bills by customer or date range
3. Click eye icon to view bill details
4. Click download icon to get PDF

## Color Scheme

The project uses smooth gradient colors:
- **Primary**: Purple gradient (#667eea to #764ba2)
- **Success**: Green gradient (#43e97b to #38f9d7)
- **Danger**: Pink gradient (#f093fb to #f5576c)
- **Info**: Blue gradient (#4facfe to #00f2fe)

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` to:
- Manage items and stock
- View and edit bills
- Monitor system data

## Future Enhancements

- User authentication and authorization
- Advanced reporting and analytics
- Export data to Excel/CSV
- Barcode scanning support
- Multi-store support
- Customer management system
- Payment tracking
- Sales trends and charts

## License

This project is open source and available for personal and commercial use.

## Support

For issues or questions, please create an issue in the project repository.
