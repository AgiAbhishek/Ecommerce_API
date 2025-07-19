from fastapi import APIRouter, HTTPException, Query, Path
from typing import Optional
from models import OrderCreate, OrderCreateResponse, OrderListResponse, OrderResponse, OrderItemResponse, ProductDetails, PaginationMetadata
from database import get_database
from utils.pagination import calculate_pagination
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=OrderCreateResponse, status_code=201)
async def create_order(order: OrderCreate):
    """Create a new order"""
    try:
        db = get_database()
        
        # Validate products exist and calculate total
        total_amount = 0.0
        validated_items = []
        
        for item in order.items:
            # Find product by string ID
            product = await db.products.find_one({"_id": item.productId})
            if not product:
                raise HTTPException(status_code=404, detail=f"Product not found: {item.productId}")
            
            # Calculate item total
            item_total = product["price"] * item.qty
            total_amount += item_total
            
            validated_items.append({
                "productId": item.productId,
                "qty": item.qty
            })
        
        # Create order document
        order_doc = {
            "userId": order.userId,
            "items": validated_items,
            "total": total_amount,
            "createdAt": datetime.utcnow().isoformat()
        }
        
        # Insert order
        result = await db.orders.insert_one(order_doc)
        
        return OrderCreateResponse(id=str(result.inserted_id))
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

@router.get("/{user_id}", response_model=OrderListResponse)
async def get_user_orders(
    user_id: str = Path(..., description="User ID to fetch orders for"),
    limit: int = Query(10, ge=1, le=100, description="Number of orders to return"),
    offset: int = Query(0, ge=0, description="Number of orders to skip")
):
    """Get orders for a specific user with product details lookup"""
    try:
        db = get_database()
        
        # Get all orders for the user
        all_orders = await db.orders.find({"userId": user_id})
        orders_data = await all_orders.to_list(length=None)
        
        # Sort by _id (creation order)
        orders_data.sort(key=lambda x: x["_id"])
        
        # Get total count for pagination
        total_count = len(orders_data)
        
        # Apply pagination
        paginated_orders = orders_data[offset:offset + limit]
        
        # Convert to response format with product details lookup
        order_responses = []
        for order in paginated_orders:
            order_items = []
            
            # Look up product details for each item
            for item in order["items"]:
                product = await db.products.find_one({"_id": item["productId"]})
                if product:
                    order_items.append(OrderItemResponse(
                        productDetails=ProductDetails(
                            name=product["name"],
                            id=product["_id"]
                        ),
                        qty=item["qty"]
                    ))
            
            order_responses.append(OrderResponse(
                id=str(order["_id"]),
                items=order_items,
                total=order["total"]
            ))
        
        # Calculate pagination metadata
        pagination = calculate_pagination(offset, limit, total_count, len(order_responses))
        
        return OrderListResponse(
            data=order_responses,
            page=pagination
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching orders: {str(e)}")
