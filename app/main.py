from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.post import PostModel
from app.routers.post import router as post_router

app = FastAPI()

# table autocreation:
Base.metadata.create_all(bind=engine)

# ROUTERS:
app.include_router(post_router)


@app.get("/")
async def root():
    return {"message":"ROOT"}

