from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    def __init__(self, detail, headers=None):
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers=headers,
        )


class IncorrectUsernameOrPasswordException(UnauthorizedException):
    def __init__(self):
        super().__init__(
            detail="Incorrect username or password",
        )


class CouldNotValidateCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__(
            detail="Could not validate credentials",
        )


class ForbiddenException(HTTPException):
    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


class InactiveUserException(ForbiddenException):
    def __init__(self):
        super().__init__(
            detail="Inactive user",
        )


class ConflictException(HTTPException):
    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
        )


class UserAlreadyExistsException(ConflictException):
    def __init__(self):
        super().__init__(
            detail="User already exists",
        )


class NotFoundException(HTTPException):
    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class UserNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__(
            detail="User not found",
        )


class BadRequestException(HTTPException):
    def __init__(self, detail):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


class AlreadyActivatedException(BadRequestException):
    def __init__(self):
        super().__init__(
            detail="User already activated",
        )


class InvalidTokenException(BadRequestException):
    def __init__(self):
        super().__init__(
            detail="Invalid token",
        )


class TokenExpiredException(BadRequestException):
    def __init__(self):
        super().__init__(
            detail="Token expired",
        )
