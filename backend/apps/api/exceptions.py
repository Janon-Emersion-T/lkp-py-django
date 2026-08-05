from typing import Any

from ninja.errors import HttpError


class ApiHttpError(HttpError):
    def __init__(
        self,
        status_code: int,
        message: str,
        *,
        code: str,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(status_code, message)

        self.code = code
        self.details = details
