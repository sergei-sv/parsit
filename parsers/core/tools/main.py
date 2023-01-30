import requests


def should_abort_request(request: requests) -> bool:
    """
    Set what resource types of request don't load in Playwright.

    :param request:
    :return: bool
    """
    if request.resource_type == 'image':
        return True

    return False


if __name__ == '__main__':
    pass
