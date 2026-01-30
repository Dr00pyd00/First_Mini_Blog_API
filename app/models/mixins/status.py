from enum import Enum as PyEnum
from sqlalchemy import Column, Enum as sqlEnum
from sqlalchemy.orm import Session

# Mon enum python:
class StatusEnum(PyEnum):
    ACTIVE = "active"
    DELETED = "deleted"
    ARCHIVED = "archived"
    SIGNALED = "signaled"


# Mixins que je peux ajouter ( Parent ) dans mes objets tables
class StatusMixin:

    status = Column(
                    sqlEnum(StatusEnum, name="status_enum"), 
                    default=StatusEnum.ACTIVE, 
                    nullable=False
                    )

    @classmethod
    def query_active(cls, session:Session):
        """return que les objets actifs"""
        return session.query(cls).filter(cls.status == StatusEnum.ACTIVE)