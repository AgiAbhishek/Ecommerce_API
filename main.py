from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes.products import router as products_router
from routes.orders import router as orders_router
from database import connect_to_mongodb
import uvicorn

app = FastAPI(
    title="Ecommerce API",
    description="FastAPI backend for ecommerce application with MongoDB. All prices are in Indian Rupees (₹).",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(products_router, prefix="/products", tags=["products"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])

@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB on startup"""
    await connect_to_mongodb()

@app.get("/")
async def root():
    """Serve the main interface"""
    return FileResponse('static/index.html')

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
