from fastapi import APIRouter, HTTPException, status
from src.test_db import categories_db, posts_db
from src.schemas.category import CategoryResponse

router = APIRouter()


@router.get(
    "/category/{category_slug}/",
    status_code=status.HTTP_200_OK,
    response_model=CategoryResponse,
)
async def category_posts(category_slug: str):
    for category in categories_db:
        if category["slug"] == category_slug:
            cat_posts = []
            for post in posts_db:
                if post["category"] == category_slug:
                    cat_posts.append(post)
                    return cat_posts
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
