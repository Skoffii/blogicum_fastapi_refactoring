class DBState:
    def __init__(self):
        self.posts_db: list[dict] = []
        self.post_id = 1

        self.categories_db: list[dict] = []
        self.category_id = 1

        self.comments_db: list[dict] = []
        self.comment_id = 1

        self.location_db: list[dict] = []
        self.location_id = 1

        self.users_db: list[dict] = []
        self.user_id = 1


db = DBState()
