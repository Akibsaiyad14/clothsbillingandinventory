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
- **Email Integration**: Automatic email delivery of PDF invoices to customers

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
- **PostgreSQL** (with camelCase table names)
- ReportLab 4.0.7 (PDF generation)
- **Python-dotenv** (environment variable management)
- **psycopg2-binary** (PostgreSQL adapter)

### Frontend
- HTML5
- CSS3 (with gradients and animations)
- Vanilla JavaScript (ES6+)
- Font Awesome icons
- JWT token storage via LocalStorage

## Installation & Setup

### Prerequisites
1. **Python 3.8+** installed
2. **PostgreSQL** installed and running
   - Download from: https://www.postgresql.org/download/
   - Remember your PostgreSQL password during installation

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

5. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Edit `.env` file with your settings:
   ```env
   # Database
   DB_NAME=clothshop_db
   DB_USER=postgres
   DB_PASSWORD=your_postgresql_password
   DB_HOST=localhost
   DB_PORT=5432
   
   # Email (Gmail example)
   EMAIL_HOST_USER=your_email@gmail.com
   EMAIL_HOST_PASSWORD=your_gmail_app_password
   DEFAULT_FROM_EMAIL=your_email@gmail.com
   ```
   
   **Gmail App Password Setup:**
   - Go to: https://myaccount.google.com/apppasswords
   - Generate a new app password
   - Use the 16-character password in `.env`

6. **Create PostgreSQL database:**
   ```powershell
   # Option 1: Using management command
   python manage.py create_database
   
   # Option 2: Using psql
   psql -U postgres -c "CREATE DATABASE clothshop_db;"
   ```

7. **Run migrations:**
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
   
   This creates tables with camelCase names:
   - `clothItems`, `stockLevels`, `customerBills`, `billItems`

8. **Create superuser (optional):**
   ```powershell
   python manage.py createsuperuser
   ```

9. **Create demo user for testing:**
   ```powershell
   python manage.py create_demo_user
   ```
   This creates a demo user with credentials: `demo` / `demo1234`

10. **Populate sample data (optional):**
    ```powershell
    python manage.py populate_items
    ```

11. **Run the development server:**
    ```powershell
    python manage.py runserver
    ```

The application will be available at `http://localhost:8000/`

**Note:** The frontend is now fully integrated into Django. No separate frontend server is needed!

### Authentication & Login

**Demo User Credentials:**
- Username: `demo`
- Password: `demo1234`

**How to Login:**
1. Go to `http://localhost:8000/login/`
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

## Accessing the Application

Once both setup steps are complete, simply start the Django server and access the application:

## Accessing the Application

Once both setup steps are complete, simply start the Django server and access the application:

```powershell
cd backend
python manage.py runserver
```

Open your browser and go to:
- **Homepage**: http://localhost:8000/ (redirects to dashboard)
- **Dashboard**: http://localhost:8000/dashboard/
- **Inventory**: http://localhost:8000/inventory/
- **Billing**: http://localhost:8000/billing/
- **Reports**: http://localhost:8000/reports/
- **Login Page**: http://localhost:8000/login/
- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

### **Login Instructions**

1. Go to http://localhost:8000/login/
2. Use demo credentials:
   - Username: `demo`
   - Password: `demo1234`
3. After login, you'll see your username in the header with a Logout button

**Important Notes:**
- The frontend is now fully integrated into Django - no separate server needed!
- All pages are served through Django's URL routing with clean URLs
- **All dates are displayed in DD-MM-YYYY format** for consistency and easy filtering
- The UI and PDF invoices use Indian Rupees (₹)
- Creating bills requires authentication (login first)
- All amounts are displayed in ₹ format
- The interface is fully responsive and mobile-friendly

## Project Structure

```
clothShops/
├── backend/
│   ├── clothshop/          # Main project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── views.py        # Template views
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
│   │   └── email_utils.py   # Email sending utility
│   ├── templates/          # Django templates
│   │   ├── dashboard.html
│   │   ├── inventory.html
│   │   ├── billing.html
│   │   ├── reports.html
│   │   └── login.html
│   ├── static/             # Static files (CSS, JS)
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── config.js
│   │       ├── dashboard.js
│   │       ├── inventory.js
│   │       ├── billing.js
│   │       └── reports.js
│   ├── .env                # Environment variables (not in git)
│   ├── .env.example        # Example environment file
│   ├── manage.py
│   └── requirements.txt
├── .git/
├── .gitignore
├── README.md
└── DATABASE_SETUP.md       # PostgreSQL setup guide
```

## Key Features

- **Clean URLs**: All pages accessible via `/dashboard/`, `/inventory/`, `/billing/`, `/reports/`, `/login/`
- **Date Format**: All dates displayed in **DD-MM-YYYY HH:MM** format for easy filtering and readability
- **Indian Rupees**: Currency displayed as ₹ throughout the application and PDFs
- **Responsive Design**: Mobile-friendly interface with collapsible navigation
- **JWT Authentication**: Secure token-based authentication
- **PostgreSQL Database**: Enterprise-grade database with camelCase table naming
- **Email Delivery**: Automatic invoice email to customers
- **Environment Variables**: Secure credential management with .env files

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
2. Enter customer information (including email for invoice delivery)
3. Search for items and add them to cart
4. Adjust quantities as needed
5. Set discount and tax rate (optional)
6. Add notes (optional)
7. Click "Create Bill"
8. PDF will automatically download **and be emailed to the customer**

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

## Security & Configuration

### Environment Variables
All sensitive credentials are stored in `.env` file:
- Database credentials (PostgreSQL)
- Email credentials (SMTP)
- Django secret key
- Debug mode settings

**Important:** Never commit `.env` file to version control!

### Email Configuration
The system uses SMTP to send invoices. For Gmail:
1. Enable 2-Step Verification
2. Generate App Password at: https://myaccount.google.com/apppasswords
3. Use app password in `.env` file

### Database Tables (camelCase)
PostgreSQL tables are named in camelCase format:
- `clothItems` - Product inventory
- `stockLevels` - Stock tracking
- `customerBills` - Sales records
- `billItems` - Bill line items

## Troubleshooting

### PostgreSQL Connection Error
- Verify PostgreSQL is running
- Check credentials in `.env` file
- Ensure database `clothshop_db` exists

### Email Not Sending
- Verify email credentials in `.env`
- Check Gmail app password is correct
- Ensure EMAIL_USE_TLS=True for Gmail
- Check firewall/antivirus settings

### Migration Errors
```powershell
python manage.py makemigrations --empty inventory
python manage.py makemigrations --empty billing
python manage.py migrate --fake
```

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
