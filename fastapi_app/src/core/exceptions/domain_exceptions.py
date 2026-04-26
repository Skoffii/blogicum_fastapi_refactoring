class BaseDomainException(Exception):
    _exception_text_template = "Произошла ошибка"

    def __init__(self, detail: str | None = None) -> None:
        self._detail = detail or self._exception_text_template
        super().__init__(self._detail)

    def get_detail(self) -> str:
        return self._detail


class UserNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пользователь с id = '{user_id}' не найден"

    def __init__(self, user_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            user_id=user_id
        )
        super().__init__(detail=self._exception_text_template)


class UserAlreadyExistExeption(BaseDomainException):
    _exception_text_template = "Пользователь с именем = '{username}' уже существует"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )
        super().__init__(detail=self._exception_text_template)


class UserNotFoundByUsernameException(BaseDomainException):
    _exception_text_template = "Пользователь с именем '{username}' не найден"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )
        super().__init__(detail=self._exception_text_template)


class UserUsernameIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с именем '{username}' уже существует"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )

        super().__init__(detail=self._exception_text_template)


class UserEmailIsNotUniqueException(BaseDomainException):
    _exception_text_template = "Пользователь с почтой '{user_email}' уже существует"

    def __init__(self, user_email: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            user_email=user_email
        )
        super().__init__(detail=self._exception_text_template)


class UserPermisionException(BaseDomainException):
    _exception_text_template = (
        "Пользователь '{current_user_id}' не имеет необходимых прав"
    )

    def __init__(self, current_user_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            current_user_id=current_user_id
        )
        super().__init__(detail=self._exception_text_template)


# Посты
class PostNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Пост с id '{post_id}' не найден"

    def __init__(self, post_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            post_id=post_id
        )
        super().__init__(detail=self._exception_text_template)


class PostHasNoImageException(BaseDomainException):
    _exception_text_template = "Пост не содержит изображения"

    def __init__(self) -> None:
        self._exception_text_template = self._exception_text_template.format()
        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundBySlugException(BaseDomainException):
    _exception_text_template = "Категория '{category_slug}' не найдена"

    def __init__(self, category_slug: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            category_slug=category_slug
        )
        super().__init__(detail=self._exception_text_template)


class CategoryNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Категория с id '{category_id}' не найдена"

    def __init__(self, category_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            category_id=category_id
        )
        super().__init__(detail=self._exception_text_template)


class CategoryNotPublishedByIdException(BaseDomainException):
    _exception_text_template = "Категория с id '{category_id}' не найдена"

    def __init__(self, category_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            category_id=category_id
        )
        super().__init__(detail=self._exception_text_template)


class CategoryAlreadyExistException(BaseDomainException):
    _exception_text_template = "Категория '{slug}' уже существует"

    def __init__(self, slug: int) -> None:
        self._exception_text_template = self._exception_text_template.format(slug=slug)
        super().__init__(detail=self._exception_text_template)


class LocationNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Локация '{location_name}' не найдена"

    def __init__(self, location_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            location_id=location_id
        )
        super().__init__(detail=self._exception_text_template)


class LocationNotFoundByNameException(BaseDomainException):
    _exception_text_template = "Локация '{location_name}' не найдена"

    def __init__(self, location_name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            location_name=location_name
        )
        super().__init__(detail=self._exception_text_template)


class LocationAlreadyExistException(BaseDomainException):
    _exception_text_template = "Локация '{location_name}' уже существует"

    def __init__(self, location_name: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            location_name=location_name
        )
        super().__init__(detail=self._exception_text_template)


class CommentNotFoundByIdException(BaseDomainException):
    _exception_text_template = "Комментарий с id '{comment_id}' не найден"

    def __init__(self, comment_id: int) -> None:
        self._exception_text_template = self._exception_text_template.format(
            comment_id=comment_id
        )
        super().__init__(detail=self._exception_text_template)


class CommentHasNoImageException(BaseDomainException):
    _exception_text_template = "Комментарий не содержит изображения"

    def __init__(self) -> None:
        self._exception_text_template = self._exception_text_template.format()
        super().__init__(detail=self._exception_text_template)


class UploadFileIsNotImageException(BaseDomainException):
    _exception_text_template = "Загруженный файл не является JPEG изображением"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text_template)


class InvalidUsernameException(BaseDomainException):
    _exception_text = "пользователь с именем {username} не найден"

    def __init__(self, username: str) -> None:
        self._exception_text_template = self._exception_text_template.format(
            username=username
        )
        super().__init__(detail=self._exception_text_template)


class WrongPasswordException(BaseDomainException):
    _exception_text = "Пароль неверен"

    def __init__(self) -> None:
        super().__init__(detail=self._exception_text)
