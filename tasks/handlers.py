import logging
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler to return consistent error responses
    """
    # Call DRF's default exception handler first
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Safely extract data from DRF's default response
        data = response.data or {}

        # If there's a "detail" key, use it; otherwise use a generic message
        message = data.get("detail", "An error occurred.")

        # Wrap everything in a consistent structure
        custom_response = {
            "status": "error",
            "message": message,
            "error": {
                "type": exc.__class__.__name__,
                "details": data,
                "status_code": response.status_code,
            },
        }
        response.data = custom_response
    else:
        # Handle unexpected server-side exceptions
        logger.exception(f"Unhandled error: {exc}")

        custom_response = {
            "status": "error",
            "message": "Internal server error.",
            "error": {
                "type": "ServerError",
                "details": None,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            },
        }
        response = Response(
            custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
