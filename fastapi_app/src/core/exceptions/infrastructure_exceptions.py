class BaseInfrastructureException(Exception):
    def __init__(self, detail: str | None = None) -> None:
        super().__init__(detail)
        self._detail = detail


class UserNotFoundById(BaseInfrastructureException):
    pass


class UserNotFoundByUsername(BaseInfrastructureException):
    pass


class UserAlreadyExist(BaseInfrastructureException):
    pass


class UserDoesNotExist(BaseInfrastructureException):
    pass


class UserEmailAlreadyExist(BaseInfrastructureException):
    pass


class UserPermissionDenied(BaseInfrastructureException):
    pass


class PostNotFoundById(BaseInfrastructureException):
    pass


class PostNotFound(BaseInfrastructureException):
    pass


class PostAlreadyExist(BaseInfrastructureException):
    pass


class PostDoesNotExist(BaseInfrastructureException):
    pass


class PostAccessDenied(BaseInfrastructureException):
    pass


class CategoryNotFoundById(BaseInfrastructureException):
    pass


class CategoryNotFoundByName(BaseInfrastructureException):
    pass


class CategoryNotPublished(BaseInfrastructureException):
    pass


class CategoryAlreadyExist(BaseInfrastructureException):
    pass


class CategoryAreadyExist(BaseInfrastructureException):
    pass


class LocationNotFoundById(BaseInfrastructureException):
    pass


class LocationNotFoundByName(BaseInfrastructureException):
    pass


class LocationAlreadyExist(BaseInfrastructureException):
    pass


class CommentNotFound(BaseInfrastructureException):
    pass


class DatabaseIntegrityError(BaseInfrastructureException):
    pass


class CredentialsException(BaseInfrastructureException):
    pass
