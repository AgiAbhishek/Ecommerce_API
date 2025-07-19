# FastAPI Ecommerce Backend - Local Setup Guide

## Prerequisites for MacBook M4 Air

### 1. Install Python 3.11+
```bash
# Check if Python is installed
python3 --version

# If not installed, install via Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python@3.11
```

### 2. Install Git (if not already installed)
```bash
git --version
# If not installed:
brew install git
```

## Project Setup Steps

### Step 1: Clone or Download the Project
```bash
# Option A: If you have the project files, create a new directory
mkdir ecommerce-api
cd ecommerce-api

# Option B: If you have a git repository
# git clone <your-repo-url>
# cd <your-repo-name>
```

### Step 2: Create Project Structure
Copy all the following files to your project directory:
- `main.py`
- `database.py`
- `models.py`
- `requirements.txt` (see below)
- `routes/products.py`
- `routes/orders.py`
- `utils/pagination.py`
- `static/index.html`

### Step 3: Create Requirements File
Create a `requirements.txt` file with these dependencies:
```txt
fastapi==0.116.1
uvicorn[standard]==0.35.0
motor==3.7.1
pymongo==4.13.2
pydantic==2.11.7
python-multipart==0.0.10
```

### Step 4: Set Up Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Step 5: Install Dependencies
```bash
# Make sure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 6: Create Directory Structure
```bash
# Create necessary directories
mkdir -p routes utils static

# Verify structure
ls -la
# You should see: main.py, database.py, models.py, routes/, utils/, static/
```

### Step 7: Run the Application
```bash
# Start the FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Alternative way:
# python main.py
```

### Step 8: Access the Application
Open your web browser and go to:
- **Main Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Project File Structure
```
ecommerce-api/
├── main.py                 # FastAPI app and routing
├── database.py            # Database connection
├── models.py              # Pydantic models
├── requirements.txt       # Python dependencies
├── routes/
│   ├── __init__.py       # Empty file (create this)
│   ├── products.py       # Product endpoints
│   └── orders.py         # Order endpoints
├── utils/
│   ├── __init__.py       # Empty file (create this)
│   └── pagination.py     # Pagination helper
├── static/
│   └── index.html        # Web interface
└── venv/                 # Virtual environment (auto-created)
```

## Important Notes

### Database Configuration
- This project uses **in-memory database** for development
- No MongoDB installation required for basic testing
- Data will be lost when you restart the server

### Currency Display
- All prices are displayed in Indian Rupees (₹)
- Enter prices as numbers (e.g., 999.99)

### Development Features
- **Auto-reload**: Changes to code automatically restart the server
- **Interactive API docs**: Available at `/docs` endpoint
- **Web interface**: Simple forms for testing all APIs

## Testing the Application

### 1. Create a Product
- Go to http://localhost:8000
- Fill in product details:
  - Name: "iPhone 15"
  - Price: 75000
  - Size: "128GB", Quantity: 10
- Click "Create Product"

### 2. Create an Order
- Select the created product from dropdown
- Enter quantity
- Click "Create Order"

### 3. View Data
- Click "Refresh Data" to see all products and orders

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
python -m uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Virtual Environment Issues
```bash
# Deactivate and recreate if needed
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Missing Files Error
Make sure you create empty `__init__.py` files:
```bash
touch routes/__init__.py
touch utils/__init__.py
```

## Production Deployment (Optional)

For production deployment, you would:
1. Set up a real MongoDB database
2. Configure environment variables
3. Use a production ASGI server
4. Set up proper logging and monitoring

## Next Steps

1. Follow this guide step by step
2. Test the application locally
3. If you encounter issues, check the troubleshooting section
4. For production deployment, consider using MongoDB Atlas for the database

## Support

If you encounter any issues:
1. Check that all files are in the correct locations
2. Ensure virtual environment is activated
3. Verify all dependencies are installed
4. Check the terminal for error messages