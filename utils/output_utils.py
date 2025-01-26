from .ansi_colors import COLORS


def print_error(error_message: str):
    """
    Prints error output in red color to the console.

    Args:
        error_message (str): Error content printed out to the console
    """
    print(f"{COLORS['RED']}{error_message}{COLORS['RESET']}")


def reset_output_color():
    print(COLORS['RESET'], end="")
