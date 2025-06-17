from slowapi import Limiter
from slowapi.util import get_remote_address
import asyncio


limiter = Limiter(key_func=get_remote_address)

file_locks = {}
file_locks_lock = asyncio.Lock()

async def get_file_lock(dataset_id: int) -> asyncio.Lock:
    async with file_locks_lock:
        if dataset_id not in file_locks:
            file_locks[dataset_id] = asyncio.Lock()
    return file_locks[dataset_id]

async def pop_file_lock(dataset_id: int) -> None:
    async with file_locks_lock:
        if dataset_id in file_locks:
            file_locks.pop(dataset_id, None)
    return
