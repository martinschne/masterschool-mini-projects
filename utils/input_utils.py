import unicodedata
from datetime import datetime

from .ansi_colors import COLORS
from .output_utils import print_error

FIRST_MOVIE_EVER_YEAR = 1878
MIN_MOVIE_RATING = 0
MAX_MOVIE_RATING = 10


def get_colored_input(prompt: str) -> str:
    """
    Set distinct color for a prompt and input, collect and return user input.

    Args:
        prompt: (str): The prompt

    Returns:
        (str) colored user input string
    """
    user_input = input(f"{COLORS['GREEN']}{prompt}{COLORS['CYAN']}")
    print(f"{COLORS['RESET']}", end="")

    return user_input


def get_normalized_input(text: str) -> str:
    """
    Normalizes text by trimming whitespace, making it case-insensitive, and removing accents.

    Args:
            text (str): The input string to normalize.

    Returns:
        str: The normalized string with accents removed and in lowercase.
    """
    normalized_text = text.strip().casefold()

    # Decompose the characters into base characters and accents
    nfkd_form = unicodedata.normalize("NFKD", normalized_text)

    # Filter out the accents and keep base characters
    base_normalized_text = ''.join(
        [char for char in nfkd_form if not unicodedata.combining(char)]
    )

    return base_normalized_text


def get_valid_rating(
        min_rating: int = MIN_MOVIE_RATING,
        max_rating: int = MAX_MOVIE_RATING,
        prompt: str | None = None,
        allow_empty_input: bool = False) -> str | float:
    """
    Prompts the user to input a valid movie rating within a specified range.
    Validates the rating. If allow_empty_input is True and the user enters empty
    string it becomes a return value of this function.

    Args:
        min_rating (int): Minimum allowed rating.
        max_rating (int): Maximum allowed rating.
        prompt (str): Default prompt is set inside a function,
            other prompt can be provided during function call.
        allow_empty_input (bool): allows empty string as a valid rating

    Returns:
        (float): The validated rating entered by the user as float or an empty string.
    """
    if prompt is None:
        prompt = f"Enter new movie rating: ({min_rating}-{max_rating}): "

    while True:
        try:
            raw_input = get_colored_input(prompt).strip()
            if allow_empty_input and raw_input == "":
                return raw_input

            user_rating = float(raw_input)
            if not min_rating <= user_rating <= max_rating:
                raise ValueError

            return user_rating
        except ValueError:
            print_error("Invalid rating")


def get_valid_year(prompt: str = None, allow_empty_input: bool = False) -> str | int:
    """
    Prompts the user to input a valid movie rating within a specified range.

    Args:
        prompt (str): Default prompt is set inside a function,
            other prompt can be provided during function call.
        allow_empty_input (bool): allows empty string as a valid year.

    Returns:
        (int): The validated year entered by the user.
    """
    current_year = datetime.now().year
    if prompt is None:
        prompt = f"Enter new movie year: ({FIRST_MOVIE_EVER_YEAR}-{current_year}): "

    while True:
        try:
            raw_input = get_colored_input(prompt).strip()
            if allow_empty_input and raw_input == "":
                return raw_input

            user_year = int(raw_input)
            if not FIRST_MOVIE_EVER_YEAR <= user_year <= current_year:
                raise ValueError

            return user_year
        except ValueError:
            print_error("Invalid year")


def get_valid_movie(prompt: str = "Enter new movie name: ") -> str:
    """
    Prompts the user to input a valid movie title.

    Args:
        prompt (str): Default prompt is set inside a function,
            other prompt can be provided during function call.
    Returns:
        (str): the validated movie title entered by the user.
    """
    while True:
        try:
            user_movie = get_colored_input(prompt).strip()
            if len(user_movie) < 1:
                raise ValueError

            return user_movie
        except ValueError:
            print_error("Movie name cannot be empty.")


def get_valid_yes_no_answer(prompt: str) -> bool:
    """Get input from user and validate its form (yes/no) or (y/n).

    Returns:
        (bool): True if lowered input was 'yes'/'y', False otherwise.
    """
    while True:
        user_response = get_colored_input(prompt).lower()
        if user_response in ['yes', 'y']:
            return True
        elif user_response in ['no', 'n']:
            return False
        else:
            print_error("Please enter 'yes' or 'no'.")


def wait_for_user_action():
    """
    Halts program execution, prompting the user to press Enter to continue.
    """
    get_colored_input("Press enter to continue")
