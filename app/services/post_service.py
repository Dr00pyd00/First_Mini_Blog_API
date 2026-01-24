from sqlalchemy.orm import Session

from app.models.post import PostModel
from app.errors_msg.post import error_post_not_found_by_id
from app.schemas.post import PostDataToCreateSchema, PostDataFromDbSchema


# Chercher un post sinon renvoyer un 404:
def get_post_by_id_or_404(post_id:int, db:Session)->PostModel | None:
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        error_post_not_found_by_id(id=post_id)
    return post


# Create post:
def create_post_service(
        data: PostDataToCreateSchema,
        db: Session,
)->PostModel:
    post = PostModel(**data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

# Update post:
def update_post_service(
    post_id: int,
    data: PostDataToCreateSchema,
    db: Session,
)->PostModel:
    post = get_post_by_id_or_404(post_id=post_id, db=db)
    for k,v in data.model_dump().items():
        setattr(post,k,v)
    db.commit()
    db.refresh(post)
    return post

# Delete post:
def delete_post_service(
    post_id: int,
    db: Session
)->None:
    post = get_post_by_id_or_404(post_id=post_id, db=db)
    db.delete(post)
    db.commit()
