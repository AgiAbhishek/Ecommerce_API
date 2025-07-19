# Ecommerce API Backend

## Overview

This is a FastAPI-based ecommerce backend application that provides REST APIs for managing products and orders. The system uses MongoDB as the primary database and follows a modular architecture with separate routing, models, and utility components. All monetary values are displayed in Indian Rupees (₹).

## User Preferences

Preferred communication style: Simple, everyday language.
Currency display: Indian Rupees (₹) instead of dollars ($).

## System Architecture

The application follows a layered architecture pattern:

- **API Layer**: FastAPI framework handling HTTP requests and responses
- **Business Logic Layer**: Route handlers implementing core business logic
- **Data Access Layer**: MongoDB integration using Motor (async MongoDB driver)
- **Model Layer**: Pydantic models for data validation and serialization

The architecture prioritizes:
- Asynchronous operations for better performance
- Clear separation of concerns
- Type safety through Pydantic models
- RESTful API design principles

## Key Components

### Database Connection (`database.py`)
- Uses Motor AsyncIOMotorClient for async MongoDB operations
- Implements connection pooling and proper connection lifecycle management
- Provides singleton pattern for database access
- Database name: `ecommerce`

### API Routes
- **Products Router** (`routes/products.py`): Handles product CRUD operations
- **Orders Router** (`routes/orders.py`): Manages order creation and retrieval
- Both routers implement proper error handling and validation

### Data Models (`models.py`)
- **Product Models**: ProductCreate, Product, ProductResponse, ProductCreateResponse
- **Order Models**: OrderItem, OrderCreate (implied from routes)
- **Utility Models**: SizeVariant, PaginationMetadata, PyObjectId
- Custom ObjectId handling for MongoDB integration

### Utilities
- **Pagination** (`utils/pagination.py`): Calculates pagination metadata for list endpoints

## Data Flow

### Product Creation Flow
1. Client sends POST request to `/products`
2. FastAPI validates request against ProductCreate model
3. Product data is stored in MongoDB products collection
4. Returns product ID in response

### Product Listing Flow
1. Client sends GET request to `/products` with optional filters
2. System builds MongoDB query with name/size filters
3. Applies pagination (limit/offset)
4. Returns paginated product list with metadata

### Order Creation Flow
1. Client sends POST request to `/orders`
2. System validates product IDs and calculates total amount
3. Order is stored in MongoDB orders collection with timestamp
4. Returns order confirmation

## External Dependencies

### Core Framework
- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running the application

### Database
- **Motor**: Async MongoDB driver for Python
- **PyMongo**: MongoDB driver (used for server API)

### Validation & Serialization
- **Pydantic**: Data validation and serialization

### CORS
- **FastAPI CORS Middleware**: Configured to allow all origins (development setup)

## Deployment Strategy

### Environment Configuration
- MongoDB connection string via `MONGODB_URL` environment variable
- Default fallback connection string provided for development

### Server Configuration
- Runs on host `0.0.0.0` port `8000`
- Includes health check endpoint at `/health`
- Startup event handler for database connection initialization

### API Documentation
- Auto-generated OpenAPI/Swagger documentation
- Title: "Ecommerce API"
- Version: "1.0.0"

## Key Architectural Decisions

### Database Choice: MongoDB
- **Problem**: Need flexible schema for product variants and orders
- **Solution**: MongoDB for document-based storage
- **Rationale**: Handles nested data structures (sizes, order items) naturally

### Async Architecture
- **Problem**: Database operations can be slow and blocking
- **Solution**: Full async/await pattern throughout the application
- **Benefits**: Better performance and scalability under load

### Pydantic Models
- **Problem**: Need strong typing and validation for API contracts
- **Solution**: Pydantic models for request/response validation
- **Benefits**: Runtime validation, automatic API documentation, type safety

### Modular Route Structure
- **Problem**: Keep codebase organized as it grows
- **Solution**: Separate router files for different resource types
- **Benefits**: Better maintainability and clear separation of concerns