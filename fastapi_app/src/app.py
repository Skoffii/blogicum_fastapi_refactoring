from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers.posts_routers import router as posts_router
from api.routers.comments_routers import router as comments_router
from api.routers.category_routers import router as category_router
from api.routers.users_routes import router as user_router
from api.routers.location_routers import router as location_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(posts_router, tags=["Posts"])
    app.include_router(category_router, tags=["Category"])
    app.include_router(comments_router, tags=["Comments"])
    app.include_router(user_router, tags=["Users"])
    app.include_router(location_router, tags=["Locations"])

    return app
