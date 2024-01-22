import http
import typing

from fastapi import status


class CustomHTTPException(Exception):
    def __init__(
        self,
        status_code: int,
        message: typing.Optional[str] = None,
        headers: typing.Optional[typing.Dict[str, str]] = None,
    ) -> None:
        if message is None:
            message = http.HTTPStatus(status_code).phrase
        self.status_code = status_code
        self.message = message
        self.headers = headers

    def __str__(self) -> str:
        return f"{self.status_code}: {self.message}"

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(code={self.status_code!r}, message={self.message!r})"


class UnauthorizedException(CustomHTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            headers={"WWW-Authenticate": "Bearer"},
        )


class IncorrectUsernameOrPasswordException(UnauthorizedException):
    def __init__(self):
        super().__init__(
            message="Incorrect username or password",
        )


class CouldNotValidateCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__(
            message="Could not validate credentials",
        )


class ForbiddenException(CustomHTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
        )


class InactiveUserException(ForbiddenException):
    def __init__(self):
        super().__init__(
            message="Inactive user",
        )


class ConflictException(CustomHTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
        )


class UserAlreadyExistsException(ConflictException):
    def __init__(self):
        super().__init__(
            message="User already exists",
        )
