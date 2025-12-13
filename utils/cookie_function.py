from django.http import HttpResponse
import json


def set_cookie_data(response, key, value, max_age=None):
    """
    Sets a cookie on the HttpResponse object.
    Value can be a string or a dictionary (will be JSON encoded).
    """
    if isinstance(value, dict):
        value = json.dumps(value)
    response.set_cookie(
        key, value, max_age=max_age, httponly=True, secure=False
    )  # Adjust secure/httponly as needed
    return response


def get_cookie_data(request, key, default=None):
    """
    Retrieves a cookie value from the HttpRequest object.
    Attempts to JSON decode the value if it looks like one.
    """
    value = request.COOKIES.get(key, default)
    if value and (value.startswith("{") or value.startswith("[")):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
    return value


def delete_cookie_data(response, key):
    """
    Deletes a cookie from the HttpResponse object.
    """
    response.delete_cookie(key)
    return response
