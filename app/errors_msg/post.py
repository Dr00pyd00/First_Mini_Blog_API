from fastapi import HTTPException, status

def error_post_not_found_by_id(id:int)-> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with ID:{id} NOT FOUND..."
    )