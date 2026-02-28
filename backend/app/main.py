from fastapi import FastAPI
from app.routers import photos 

app = FastAPI()

app.include_router(photos.router)

@app.get("/")
def read_root():
    return {"message": "Backend Running"}


