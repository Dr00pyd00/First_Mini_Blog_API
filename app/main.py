from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.post import PostModel

app = FastAPI()

# table autocreation:
Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message":"ROOT"}

