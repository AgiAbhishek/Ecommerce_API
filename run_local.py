#!/usr/bin/env python3
"""
Local development server script for FastAPI Ecommerce Backend
Run this script to start the development server on your MacBook
"""

import uvicorn
import sys
import os

def main():
    """Start the FastAPI development server"""
    print("🚀 Starting FastAPI Ecommerce Backend...")
    print("📱 Currency: Indian Rupees (₹)")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation at: http://localhost:8000/docs")
    print("🔄 Auto-reload is enabled - changes will restart the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()