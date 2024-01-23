from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
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


class ForbiddenException(HTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
        )


class InactiveUserException(ForbiddenException):
    def __init__(self):
        super().__init__(
            message="Inactive user",
        )


class ConflictException(HTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )


class UserAlreadyExistsException(ConflictException):
    def __init__(self):
        super().__init__(
            message="User already exists",
        )


class NotFoundException(HTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )


class UserNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(
            message="User not found",
        )


class BadRequestException(HTTPException):
    def __init__(self, message):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message,
        )


class AlreadyActivatedException(BadRequestException):
    def __init__(self):
        super().__init__(
            message="User already activated",
        )


class InvalidTokenException(BadRequestException):
    def __init__(self):
        super().__init__(
            message="Invalid token",
        )


class TokenExpiredException(BadRequestException):
    def __init__(self):
        super().__init__(
            message="Token expired",
        )
