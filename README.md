# ShipTrack Pro - Django Shipping Management System

A comprehensive Django web application for managing shipping and logistics operations with an Excel-like admin interface and client tracking portal.

## Features

### Admin Features (Excel-like Interface)
- **Jazzmin-powered Admin**: Modern, customizable admin interface
- **Comprehensive Shipment Management**: Track all aspects of shipments from BL numbers to delivery
- **Excel-like Editing**: Direct list editing with search, filters, and bulk actions
- **Import/Export**: Full CSV/Excel import and export functionality using django-import-export
- **Advanced Search**: Search by BL Number, Container Number, Chassis Number, and more
- **Status Tracking**: Real-time status updates with color-coded indicators
- **Financial Tracking**: Duty payments, freight charges, and port expenses

### Client Features
- **Modern Tracking Interface**: Clean, responsive design inspired by industry leaders
- **Real-time Updates**: Track shipments using BL Number, Container Number, or Chassis Number
- **Comprehensive Details**: View all relevant shipment information
- **Mobile Responsive**: Works perfectly on all devices
- **Professional Design**: Modern UI with smooth animations and interactions

## Installation

### Prerequisites
- Python 3.12+
- PostgreSQL (for production)
- Git

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd shipping-management-system
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Database setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

### Production Setup

For production deployment:

1. **Update settings.py**:
   - Uncomment the PostgreSQL database configuration
   - Set environment variables for database connection
   - Update `ALLOWED_HOSTS`
   - Set `DEBUG = False`

2. **Environment Variables**:
   ```bash
   export DB_NAME=your_db_name
   export DB_USER=your_db_user
   export DB_PASSWORD=your_db_password
   export DB_HOST=your_db_host
   export DB_PORT=5432
   ```

## Usage

### Admin Interface

1. **Access**: Navigate to `/admin/` and login with superuser credentials
2. **Add Shipments**: Click "Add Shipment" to create new records
3. **Excel-like Editing**: Use list view for quick editing of multiple records
4. **Import Data**: Use "Import" button to upload CSV/Excel files
5. **Export Data**: Use "Export" to download data in various formats
6. **Search & Filter**: Use the search bar and filters for quick data access

### Client Tracking

1. **Access**: Navigate to the home page
2. **Enter Tracking Number**: Input BL Number, Container Number, or Chassis Number
3. **View Results**: Get comprehensive shipment details instantly

## Model Structure

### Shipment Model Fields

**Basic Information**:
- BL Number (unique identifier)
- Container Number
- Chassis Number
- Shipping Line
- Consignee
- Shipper
- Description

**Timeline & Status**:
- ETA (Expected Time of Arrival)
- Gate Out Date
- Free Days
- Demurrage Days

**Financial Information**:
- Duty Status (Paid/Not Paid)
- Penalty Duty Amount
- Freight Payment Amount
- Freight Status (Paid/Not Paid/Pending)
- Extra Charges at Port
- Towing Charges

**Management**:
- Agent Assigned
- Supervisor Status
- Towing Information

## Customization

### Admin Interface Customization

The admin interface is powered by **Jazzmin** and can be customized in `settings.py`:

```python
JAZZMIN_SETTINGS = {
    "site_title": "Your Company Name",
    "site_header": "Your Header",
    # ... more customization options
}
```

### UI Customization

- **Colors**: Update CSS custom properties in `base.html`
- **Logo**: Add your logo in Jazzmin settings
- **Branding**: Update navbar brand and titles

## API Endpoints

- `POST /api/track/` - Track shipment (AJAX)
- `GET /api/status/` - Get shipment status (JSON API)
- `GET /shipment/<tracking_number>/` - Detailed shipment view

## Database

### Local Development
Uses SQLite by default for easy setup.

### Production
Configured for PostgreSQL with environment variables.

## Security Features

- CSRF protection enabled
- SQL injection protection through Django ORM
- XSS protection with template escaping
- Secure headers with middleware
- Environment-based configuration

## Performance Optimization

- Database indexes on frequently queried fields
- Efficient querysets with select_related
- Static file compression with WhiteNoise
- Responsive design for faster mobile loading

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For support and questions:
- Check the Django documentation
- Review the Jazzmin documentation
- Check issues in the repository

## License

This project is licensed under the MIT License.

---

**ShipTrack Pro** - Professional shipping management made simple.