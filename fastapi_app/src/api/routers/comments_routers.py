from fastapi import ApiRouter, HTTPExeptions, status
from typing import List
from test_db import posts_db, comments_db
from schemas.comments import CommentRequest, CommentUpdate, CommentResponse
from datetime import datetime

router = ApiRouter(prefix = "/posts/{post_id}/")
