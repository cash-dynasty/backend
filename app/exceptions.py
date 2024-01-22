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
