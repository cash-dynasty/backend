import exceptions as exc_module
import schemas.response


def generate_responses_for_doc(exceptions: list):
    result = {}
    for exception in exceptions:
        try:
            exc_func = getattr(exc_module, exception)
            exc = exc_func()
            result.update(
                {
                    exc.status_code: {
                        "description": exc.detail,
                        "model": schemas.response.MessageRes,
                    },
                }
            )
        except AttributeError:
            print(f"Invalid exception: {exception}")
    return result
