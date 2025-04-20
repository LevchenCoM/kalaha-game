from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from .dependencies import errors


async def storage_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"error": "Object is not found in storage", "detail": str(exc)},
    )


def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(errors.DoesNotExist, storage_error_handler)
    app.add_exception_handler(errors.NotUnique, storage_error_handler)
