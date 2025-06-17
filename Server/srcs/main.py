from database import lifespan
from fastapi import FastAPI
from router import router

app = FastAPI(lifespan=lifespan)
app.include_router(router=router)
