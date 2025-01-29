from typing import Callable
from urllib.parse import urlparse

from .ansi_colors import COLORS


def print_error(error_message: str):
    """
    Prints error output in red color to the console.

    Args:
        error_message (str): Error content printed out to the console
    """
    print(f"{COLORS['RED']}{error_message}{COLORS['RESET']}")


def reset_output_color():
    """
    Resets the terminal output color to the default.

    This function prints the reset color escape sequence defined
    in the `COLORS` dictionary. It is useful for ensuring that the
    terminal text color is set back to its default after colored
    output.
    """
    print(COLORS['RESET'], end="")


def convert_to_number(value: str, conversion_func: Callable) -> int | float | None:
    """
    Converts a value to a number using a specified conversion function.

    This function attempts to convert the given value into a number
    using the provided conversion function (e.g., `int`, `float`). If the
    conversion fails (raises a `ValueError`), it returns `None`.

    Args:
        value (str): The input value to convert.
        conversion_func (Callable): The function to use for conversion (e.g., `int`, `float`).

    Returns:
        Union[int, float, None]: The converted number if successful, otherwise `None`.

    Example:
        >>> convert_to_number("123", int)
        123
        >>> convert_to_number("abc", int)
        None
        >>> convert_to_number("3.14", float)
        3.14
    """
    try:
        return conversion_func(value)
    except ValueError:
        return None


def validate_url(url: str) -> str | None:
    """Validates a given URL and returns it if valid, otherwise returns None.

    This function checks whether the provided URL has both a scheme
    (e.g., "http" or "https") and a network location (domain). If the URL
    is valid, it returns the original URL; otherwise, it returns None.

    Args:
        url (str): The URL to validate.

    Returns:
        str | None: The original URL if valid, otherwise None.

    Example:
        >>> validate_url("https://example.com")
        'https://example.com'
        >>> validate_url("invalid-url")
        None
    """
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return url
    return None
