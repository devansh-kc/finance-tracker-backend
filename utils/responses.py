from rest_framework.response import Response
from rest_framework import status


def standard_response(
    success=True, message="", data=None, errors=None, status_code=status.HTTP_200_OK
):
    """
    Generate a standardized API response
    """
    return Response(
        {
            "success": success,
            "status": status_code,
            "message": message,
            "data": data,
            "errors": errors,
        },
        status=status_code,
    )
