from pydantic import BaseModel
from datetime import datetime


# Create a user:
class UserCreateSchema(BaseModel):
    username: str
    password: str
    is_active : bool = True


#  Data client can see:
class UserDataFromDbSchema(BaseModel):
    id: int
    username: str
    is_active : bool
    created_at : datetime
