from pydantic import BaseModel, Field
from typing import List, Optional

class SizeVariant(BaseModel):
    size: str
    quantity: int = Field(ge=0)

class ProductCreate(BaseModel):
    name: str
    price: float = Field(gt=0)
    sizes: List[SizeVariant]

class Product(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    price: float
    sizes: List[SizeVariant]

    class Config:
        populate_by_name = True

class ProductResponse(BaseModel):
    id: str
    name: str
    price: float

class ProductCreateResponse(BaseModel):
    id: str

class OrderItem(BaseModel):
    productId: str
    qty: int = Field(gt=0)

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class OrderCreateResponse(BaseModel):
    id: str

class ProductDetails(BaseModel):
    name: str
    id: str

class OrderItemResponse(BaseModel):
    productDetails: ProductDetails
    qty: int

class OrderResponse(BaseModel):
    id: str
    items: List[OrderItemResponse]
    total: float

class PaginationMetadata(BaseModel):
    next: Optional[str] = None
    limit: int
    previous: Optional[str] = None

class ProductListResponse(BaseModel):
    data: List[ProductResponse]
    page: PaginationMetadata

class OrderListResponse(BaseModel):
    data: List[OrderResponse]
    page: PaginationMetadata

class Order(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    userId: str
    items: List[OrderItem]
    total: float
    createdAt: Optional[str] = None

    class Config:
        validate_by_name = True
