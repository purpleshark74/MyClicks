from fastapi import FastAPI
from app.routers import photos, comments
from app.database import Base, engine
from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(photos.router)
app.include_router(comments.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Backend Running"}


