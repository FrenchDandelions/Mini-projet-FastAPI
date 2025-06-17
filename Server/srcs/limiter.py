from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio


def limit_by_method_and_endpoint(request):
    """
    Generate a unique key for rate limiting based on client IP, HTTP method, and endpoint path.
    """
    ip = get_remote_address(request)
    method = request.method
    path = request.url.path
    return f"{ip}:{method}:{path}"

limiter = Limiter(key_func=limit_by_method_and_endpoint)


file_locks = {}
file_locks_lock = asyncio.Lock()

async def get_file_lock(dataset_id: int) -> asyncio.Lock:
    """Get or create an asyncio lock for a specific dataset ID."""
    async with file_locks_lock:
        if dataset_id not in file_locks:
            file_locks[dataset_id] = asyncio.Lock()
    return file_locks[dataset_id]

async def pop_file_lock(dataset_id: int) -> None:
    """Remove an asyncio lock for a specific dataset ID."""
    async with file_locks_lock:
        if dataset_id in file_locks:
            file_locks.pop(dataset_id, None)
    return
