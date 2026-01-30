from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text

from app.core.database import Base
from app.models.mixins.status import StatusMixin


class PostLike(StatusMixin, Base):
    __tablename__ = "postlikes"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))
    like_type = Column(String, nullable=False, server_default=text("'Normal'"))


    # application d'une contrainte 
    __table_args__ = (
        UniqueConstraint("user_id", "post_id", 
                         name= "uq_postlike_user_post"),
    )

    # relationships:
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")





# ANCIENNE METHODE :
# un like banal donc juste une relation user/post  qui met un like
# Changement: j'ai mis des fileds en plus donc le like devient un objeten soit.

# class PostLike(Base):
#     __tablename__ = "postlikes"
#     # pas de id on s'en fou
#     user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True )
#     post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
#     created_at = Column(TIMESTAMP(timezone=True), server_default=text("NOW()"))

#     post_liked = relationship("Post", back_populates="likes")
#     like_owner = relationship("User", back_populates="likes")