import asyncio
import asyncpg
from fastapi import FastAPI
from .routers import health, todos

app = FastAPI()

app.include_router(health.router)
app.include_router(todos.router)

@app.on_event('startup')
async def startup():
    app.pool = await asyncpg.create_pool(user = 'postgres',
                                        database = 'todos',
                                        password = 'local',
                                        min_size = 1,
                                        max_size = 3)
    return

@app.get('/')
async def root():
    return {'message' : 'Basic Todo Application'}