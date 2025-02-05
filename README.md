# Sales Dashboard with Django

A real-time sales analytics dashboard built with Django and PostgreSQL, featuring interactive charts, sales management, and inventory tracking.

## Features

### Sales Management
- **CRUD operations** for sales records
- Product inventory management with stock validation
- Automatic total price calculation (Quantity × Price)
- Salesperson performance tracking

### Dashboard Analytics
- Total monthly revenue & sales count
- Weekly revenue trends visualization
- Top 5 selling products by quantity
- Revenue breakdown by salesperson (pie chart)
- Daily sales trends (line chart)
- Low-stock alerts (<5 units remaining)

### Technical Highlights
- 🐳 Docker containerization support
- 📊 Interactive charts using Chart.js
- ⚡ Real-time data updates
- 🔍 Filtering by date range, salesperson, and product
- 📱 Responsive design

## Technologies Used

- **Backend**: Django 5.1, Python 3.10
- **Database**: PostgreSQL
- **Frontend**: Chart.js, HTML5, CSS3
- **Containerization**: Docker, Docker Compose

## Installation

### Prerequisites
- Docker & Docker Compose (recommended)
- Python 3.10+ and PostgreSQL 14+ (for manual setup)

### Using Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/sales-dashboard.git
cd sales-dashboard

# Build and start containers
docker-compose up --build

# Access the application at:
http://localhost:8000
```

## Manual Setup

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure PostgreSQL database:
1. Create database named 'sales_db'
2. Create user 'admin' with password 'admin123'

# Run migrations and seed data
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver

# Access the application at:
http://localhost:8000
```

## Configuration

- POSTGRES_DB = 'sales_db'
- POSTGRES_USER = 'admin'
- POSTGRES_PASSWORD = 'admin123'

### Usage

## Dashboard: http://localhost:8000

- Apply filters using date range, salesperson, or product
- Interactive hover effects on charts
- Real-time data updates

## Add Sales: http://localhost:8000/sales/add/

- Select from available products with stock
- Automatic total price calculation

## Manage Products: http://localhost:8000/stocks

- Add new products
- View current stock levels
- Low-stock warnings highlighted

## View All Sales: http://localhost:8000/sales/


