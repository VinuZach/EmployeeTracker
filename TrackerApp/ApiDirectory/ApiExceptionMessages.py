from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    print("inside exception ")
    if response is not None:
        occurredException = exc.__class__.__name__
        print(occurredException)
        customHandler = {"AuthenticationFailed": handleAuthException(response),
                         "Internal Server Error": handleInternalServerException(response),
                         "MethodNotAllowed": handleInvalidMethod(response)

                         }
        if occurredException in customHandler:
            print("asdsd")
            return customHandler.get(occurredException)
        else:
            response.data['status_code'] = response.status_code
            return response
    else:
        return "error"


def handleInternalServerException(response):
    response.data = {
        "message": "userUnauthorised",
        "status_code": response.status_code
    }
    return response


def handleAuthException(response):
    response.data = {
        "message": "userUnauthorised",
        "status_code": "200"
    }
    return response


def handleInvalidMethod(response):
    response.data = {
        "message": "Invalid api",
        "status_code": "405"
    }
    return response
