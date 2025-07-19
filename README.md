# FastAPI Ecommerce Backend API

A comprehensive FastAPI-based ecommerce backend application with MongoDB Atlas integration, featuring product management and order processing capabilities. All monetary values are displayed in Indian Rupees (₹).

## Features

- **Product Management**: Create, list, and filter products with size variants
- **Order Management**: Create orders and retrieve user-specific order history
- **MongoDB Atlas Integration**: Cloud-based persistent data storage
- **RESTful API Design**: Clean, well-documented API endpoints
- **Interactive Web Interface**: Built-in testing interface with form-based inputs
- **Pagination Support**: Efficient data retrieval with limit/offset pagination
- **Advanced Filtering**: Search products by name and size
- **Automatic Validation**: Pydantic models for data validation
- **Indian Currency Support**: All prices displayed in Rupees (₹)

## Technology Stack

- **Backend Framework**: FastAPI 0.116.1
- **Database**: MongoDB Atlas (Cloud)
- **Database Driver**: Motor (Async MongoDB driver)
- **Validation**: Pydantic 2.11.7
- **Server**: Uvicorn (ASGI server)
- **Language**: Python 3.11+

## Project Structure

```
ecommerce-api/
├── main.py                     # FastAPI application and routing
├── database.py                 # Database connection and configuration
├── models.py                   # Pydantic data models
├── routes/
│   ├── __init__.py
│   ├── products.py             # Product CRUD endpoints
│   └── orders.py               # Order management endpoints
├── utils/
│   ├── __init__.py
│   └── pagination.py           # Pagination helper functions
├── static/
│   └── index.html              # Interactive web testing interface
├── README.md                   # Project documentation
├── local_requirements.txt      # Python dependencies
└── run_local.py                # Development server launcher
```

## Prerequisites

- **Python 3.11 or higher**
- **MongoDB Atlas account** (free tier available)
- **Git** (for version control)
- **Homebrew** (for macOS package management)

## Quick Start

### 1. Clone and Setup Project

```bash
# Create project directory
mkdir ecommerce-api
cd ecommerce-api

# Copy all project files to this directory
# (Download from source or copy from existing project)
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Verify activation (should show (venv) in prompt)
```

### 3. Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r local_requirements.txt
```

### 4. Setup MongoDB Atlas

#### Option A: Quick Setup (Recommended)
```bash
# Run automated setup script
python setup_atlas_only.py
```

#### Option B: Manual Setup
1. Visit [MongoDB Atlas](https://www.mongodb.com/atlas)
2. Create free account and M0 cluster
3. Create database user with username/password
4. Configure network access (allow all IPs for development)
5. Get connection string from "Connect" button

### 5. Configure Environment

```bash
# Set MongoDB connection string
export MONGODB_URL="mongodb+srv://username:password@cluster.mongodb.net/ecommerce"

# Add to shell profile for persistence
echo 'export MONGODB_URL="your_connection_string"' >> ~/.zshrc
source ~/.zshrc
```

### 6. Run the Application

```bash
# Start development server
python run_local.py

# Alternative methods:
# python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# python main.py
```

### 7. Access the Application

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## API Endpoints

### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/products` | Create a new product |
| `GET` | `/products` | List all products with filtering and pagination |

### Orders

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/orders` | Create a new order |
| `GET` | `/orders/{user_id}` | Get orders for a specific user |

### System

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface for API testing |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/docs` | Interactive API documentation |

## Data Models

### Product
```json
{
  "name": "iPhone 15",
  "price": 75000.00,
  "sizes": [
    {
      "size": "128GB",
      "quantity": 10
    },
    {
      "size": "256GB",
      "quantity": 5
    }
  ]
}
```

### Order
```json
{
  "userId": "user_1",
  "items": [
    {
      "productId": "product_id_here",
      "qty": 2
    }
  ]
}
```

## Usage Examples

### Creating a Product
```bash
curl -X POST "http://localhost:8000/products" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "iPhone 15",
       "price": 75000.00,
       "sizes": [
         {"size": "128GB", "quantity": 10},
         {"size": "256GB", "quantity": 5}
       ]
     }'
```

### Listing Products with Filters
```bash
curl "http://localhost:8000/products?name=iPhone&size=128GB&limit=10&offset=0"
```

### Creating an Order
```bash
curl -X POST "http://localhost:8000/orders" \
     -H "Content-Type: application/json" \
     -d '{
       "userId": "user_1",
       "items": [
         {"productId": "product_id", "qty": 1}
       ]
     }'
```

### Getting User Orders
```bash
curl "http://localhost:8000/orders/user_1?limit=10&offset=0"
```

## Web Interface Usage

1. Open http://localhost:8000 in your browser
2. Use the **Products Management** section to:
   - Create products with multiple size variants
   - List and filter existing products
3. Use the **Orders Management** section to:
   - Create orders by selecting products from dropdown
   - View user order history
4. Use the **Current Data** section to:
   - View all stored products and orders
   - Refresh data to see latest changes

## Development Features

### Auto-reload
The development server automatically restarts when you make code changes.

### Interactive Documentation
Visit `/docs` for Swagger UI with interactive API testing capabilities.

### Logging
Application logs show database connection status and API request details.

### Error Handling
Comprehensive error handling with meaningful HTTP status codes and messages.

## Database Collections

### Products Collection
- Stores product information with embedded size variants
- Indexed on `name` for faster text searches
- Supports regex-based name filtering

### Orders Collection
- Stores order data with user references
- Indexed on `userId` for efficient user-specific queries
- Includes automatic timestamp generation

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URL` | MongoDB Atlas connection string | Required |
| `DATABASE_NAME` | Database name in MongoDB | `ecommerce` |

## Troubleshooting

### Common Issues

**1. Connection Refused**
```bash
# Check if MongoDB URL is set
echo $MONGODB_URL

# Verify Atlas cluster is running
# Check network access configuration in Atlas
```

**2. Authentication Failed**
- Verify username and password in connection string
- Check if database user has proper permissions
- Ensure special characters in password are URL encoded

**3. Import Errors**
```bash
# Reinstall dependencies
pip install --force-reinstall -r local_requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

**4. Port Already in Use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Performance Optimization

- Database indexes are automatically created for frequently queried fields
- Connection pooling is handled by Motor driver
- Pagination is implemented to handle large datasets efficiently

## Production Deployment

For production deployment:

1. **Environment**: Set production MongoDB Atlas cluster
2. **Security**: Configure proper network access rules
3. **Monitoring**: Set up logging and health monitoring
4. **Scaling**: Consider MongoDB Atlas auto-scaling features
5. **SSL**: Ensure HTTPS in production environment
