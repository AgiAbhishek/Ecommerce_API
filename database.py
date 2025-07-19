import os
from typing import Dict, List, Any, Optional
import uuid

class InMemoryDatabase:
    def __init__(self):
        self.products: List[Dict[str, Any]] = []
        self.orders: List[Dict[str, Any]] = []

    async def insert_one(self, collection: str, document: Dict[str, Any]) -> Dict[str, str]:
        """Insert a document into a collection"""
        doc_id = str(uuid.uuid4())
        document["_id"] = doc_id
        
        if collection == "products":
            self.products.append(document)
        elif collection == "orders":
            self.orders.append(document)
        
        class InsertResult:
            def __init__(self, doc_id):
                self.inserted_id = doc_id
        return InsertResult(doc_id)

    async def find_one(self, collection: str, query: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Find a single document"""
        data = self.products if collection == "products" else self.orders
        
        for doc in data:
            if all(doc.get(k) == v for k, v in query.items()):
                return doc
        return None

    async def find(self, collection: str, query: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Find multiple documents"""
        data = self.products if collection == "products" else self.orders
        
        if not query:
            return data
        
        results = []
        for doc in data:
            match = True
            for key, value in query.items():
                if key == "sizes" and "$elemMatch" in value:
                    # Handle size filtering
                    size_query = value["$elemMatch"]
                    if not any(size.get("size") == size_query.get("size") for size in doc.get("sizes", [])):
                        match = False
                        break
                elif key == "name" and "$regex" in value:
                    # Handle name regex filtering
                    import re
                    pattern = value["$regex"]
                    if not re.search(pattern, doc.get("name", ""), re.IGNORECASE):
                        match = False
                        break
                elif doc.get(key) != value:
                    match = False
                    break
            
            if match:
                results.append(doc)
        
        return results

    async def count_documents(self, collection: str, query: Dict[str, Any] = None) -> int:
        """Count documents matching query"""
        results = await self.find(collection, query)
        return len(results)

# Global database instance
db_instance = InMemoryDatabase()

class DatabaseCollection:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    async def insert_one(self, document: Dict[str, Any]):
        return await db_instance.insert_one(self.collection_name, document)

    async def find_one(self, query: Dict[str, Any]):
        return await db_instance.find_one(self.collection_name, query)

    def find(self, query: Dict[str, Any] = None):
        class Cursor:
            def __init__(self, collection_name, query):
                self.collection_name = collection_name
                self.query = query
                self._skip = 0
                self._limit = None
                self._sort = None

            def skip(self, num):
                self._skip = num
                return self

            def limit(self, num):
                self._limit = num
                return self

            def sort(self, field, direction):
                self._sort = (field, direction)
                return self

            async def to_list(self, length):
                results = await db_instance.find(self.collection_name, self.query)
                data = results
                if self._sort:
                    field, direction = self._sort
                    data = sorted(data, key=lambda x: x.get(field, ""), reverse=(direction == -1))
                
                data = data[self._skip:]
                if self._limit:
                    data = data[:self._limit]
                
                return data

        return Cursor(self.collection_name, query)

    async def count_documents(self, query: Dict[str, Any] = None):
        return await db_instance.count_documents(self.collection_name, query)

class Database:
    @property
    def products(self):
        return DatabaseCollection("products")

    @property
    def orders(self):
        return DatabaseCollection("orders")

# Global database object
database = Database()

async def connect_to_mongodb():
    """Initialize in-memory database"""
    print("Using in-memory database for development")

def get_database():
    return database
