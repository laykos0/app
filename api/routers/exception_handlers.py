from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from infrastructure.exceptions import CustomException


async def handle_404_not_found(request: Request, exc: CustomException):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={"message": str(exc), "error_type": exc.error_type})
