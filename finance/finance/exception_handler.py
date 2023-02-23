from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        error_object = {"error": exc.detail}
        response.data = response.get("data", {})
        response.data.pop("detail", None)
        response.data["info"] = error_object
    return response
