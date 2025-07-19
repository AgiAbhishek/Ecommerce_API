from models import PaginationMetadata
from typing import Optional

def calculate_pagination(offset: int, limit: int, total_count: int, current_page_count: int) -> PaginationMetadata:
    """Calculate pagination metadata"""
    
    # Calculate next page offset
    next_offset = None
    if offset + limit < total_count:
        next_offset = str(offset + limit)
    
    # Calculate previous page offset
    previous_offset = None
    if offset > 0:
        previous_offset = str(max(0, offset - limit))
    
    return PaginationMetadata(
        next=next_offset,
        limit=current_page_count,
        previous=previous_offset
    )
