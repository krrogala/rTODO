# services/todo_api/initialize_db.py

import asyncio

from fastapi_todo.database import init_db

loop = asyncio.get_event_loop()
loop.run_until_complete(init_db())
