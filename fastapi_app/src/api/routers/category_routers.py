from fastapi import APIRouter, HTTPException, status
from test_db import db
from schemas.category import CategoryResponse
from typing import List

router = APIRouter()


@router.get("/category/{category_slug}/", status_code=status.HTTP_200_OK, response_model=List[CategoryResponse])
async def category_posts(category_slug: str):
    category_exists = any(cat["slug"] == category_slug for cat in db.categories_db)
    if not category_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    cat_posts = []
    for post in db.posts_db:
        if post.get("category") == category_slug:
            cat_posts.append(post)
    if not cat_posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return cat_posts
