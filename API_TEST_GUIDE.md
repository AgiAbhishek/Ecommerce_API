# 🛒 Ecommerce API Testing Guide

## How to Test Your API

### Method 1: Web Interface (Easiest)
1. **Open your browser** and go to: `http://localhost:5000` or use the Replit preview
2. **You'll see a user-friendly web interface** with forms to test all endpoints
3. **Use the interface to:**
   - Create products with name, price, and sizes
   - List products with filters
   - Create orders with multiple items
   - View user orders with product details

### Method 2: FastAPI Interactive Docs
1. **Go to:** `http://localhost:5000/docs`
2. **This shows all API endpoints** with interactive testing
3. **Click "Try it out"** on any endpoint to test it directly

### Method 3: Using curl commands

#### 1. Create a Product
```bash
curl -X POST "http://localhost:5000/products" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "T-Shirt",
       "price": 25.99,
       "sizes": [
         {"size": "large", "quantity": 10},
         {"size": "medium", "quantity": 5}
       ]
     }'
```

#### 2. List Products
```bash
# List all products
curl "http://localhost:5000/products"

# Filter by name
curl "http://localhost:5000/products?name=shirt"

# Filter by size
curl "http://localhost:5000/products?size=large"

# With pagination
curl "http://localhost:5000/products?limit=5&offset=0"
```

#### 3. Create an Order
```bash
curl -X POST "http://localhost:5000/orders" \
     -H "Content-Type: application/json" \
     -d '{
       "userId": "user_1",
       "items": [
         {"productId": "PRODUCT_ID_HERE", "qty": 2}
       ]
     }'
```

#### 4. Get User Orders
```bash
curl "http://localhost:5000/orders/user_1"
```

## Sample Test Flow

1. **Create a Product:**
   - Name: "Smartphone"
   - Price: 699.99
   - Sizes: [{"size": "128GB", "quantity": 5}, {"size": "256GB", "quantity": 3}]

2. **List Products:**
   - Should show your created product

3. **Create an Order:**
   - Use the product ID from step 1
   - Quantity: 1

4. **Get Orders:**
   - Should show your order with product details

## Expected API Responses

### Product Creation Response:
```json
{
  "id": "12345678-1234-1234-1234-123456789012"
}
```

### Product List Response:
```json
{
  "data": [
    {
      "id": "12345678-1234-1234-1234-123456789012",
      "name": "Smartphone",
      "price": 699.99
    }
  ],
  "page": {
    "next": null,
    "limit": 1,
    "previous": null
  }
}
```

### Order Creation Response:
```json
{
  "id": "87654321-4321-4321-4321-210987654321"
}
```

### Order List Response:
```json
{
  "data": [
    {
      "id": "87654321-4321-4321-4321-210987654321",
      "items": [
        {
          "productDetails": {
            "name": "Smartphone",
            "id": "12345678-1234-1234-1234-123456789012"
          },
          "qty": 1
        }
      ],
      "total": 699.99
    }
  ],
  "page": {
    "next": null,
    "limit": 1,
    "previous": null
  }
}
```

## Status Codes
- `200` - Success (GET requests)
- `201` - Created (POST requests)
- `400` - Bad Request (invalid data)
- `404` - Not Found (product doesn't exist)
- `500` - Server Error

## Tips for Testing
1. **Always create products first** before creating orders
2. **Copy the product ID** from the create response to use in orders
3. **Use the web interface** for the easiest testing experience
4. **Check the "Current Data" section** in the web interface to see all stored data