from fastapi import HTTPException, status


class UserAlreadyExistsError(HTTPException):
    """Raised when trying to create a user with an existing email."""
    def __init__(self, status_code: int = status.HTTP_400_BAD_REQUEST, detail: str = "User already exists"):
        super().__init__(status_code, detail)


class UserNotFound(HTTPException):
    def __init__(self, status_code: int = status.HTTP_404_NOT_FOUND, detail: str = "User not found"):
        super().__init__(status_code, detail)
