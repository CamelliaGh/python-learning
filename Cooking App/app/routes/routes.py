from fastapi import FastAPI
from .recipes import router as recipes_router

app = FastAPI()
app.include_router(recipes_router)