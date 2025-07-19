from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models import ProductCreate, ProductCreateResponse, ProductListResponse, ProductResponse, PaginationMetadata
from database import get_database
from utils.pagination import calculate_pagination
import re

router = APIRouter()

@router.post("", response_model=ProductCreateResponse, status_code=201)
async def create_product(product: ProductCreate):
    """Create a new product"""
    try:
        db = get_database()
        
        # Convert product to dict and insert
        product_dict = product.dict()
        result = await db.products.insert_one(product_dict)
        
        return ProductCreateResponse(id=str(result.inserted_id))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating product: {str(e)}")

@router.get("", response_model=ProductListResponse)
async def list_products(
    name: Optional[str] = Query(None, description="Filter by product name (supports regex)"),
    size: Optional[str] = Query(None, description="Filter by size availability"),
    limit: int = Query(10, ge=1, le=100, description="Number of products to return"),
    offset: int = Query(0, ge=0, description="Number of products to skip")
):
    """List products with optional filtering and pagination"""
    try:
        db = get_database()
        
        # Build query filter
        query_filter = {}
        
        # Name filter with regex support
        if name:
            query_filter["name"] = {"$regex": re.escape(name), "$options": "i"}
        
        # Size filter - check if any size variant matches
        if size:
            query_filter["sizes"] = {"$elemMatch": {"size": size}}
        
        # Get total count for pagination
        total_count = await db.products.count_documents(query_filter)
        
        # Execute query with pagination
        cursor = db.products.find(query_filter).skip(offset).limit(limit).sort("_id", 1)
        products = await cursor.to_list(length=limit)
        
        # Convert to response format (exclude sizes from output)
        product_responses = [
            ProductResponse(
                id=str(product["_id"]),
                name=product["name"],
                price=product["price"]
            )
            for product in products
        ]
        
        # Calculate pagination metadata
        pagination = calculate_pagination(offset, limit, total_count, len(product_responses))
        
        return ProductListResponse(
            data=product_responses,
            page=pagination
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching products: {str(e)}")
