import movies_storage

import random
import re
import statistics
import sys
import unicodedata
from difflib import get_close_matches
# pylint: disable=import-error
import matplotlib
import matplotlib.pyplot as plt

# Use the Agg backend for rendering to a file
matplotlib.use('Agg')

MENU_ITEMS = [
    "Exit",
    "List movies",
    "Add movie",
    "Delete movie",
    "Update movie",
    "Stats",
    "Random movie",
    "Search movie",
    "Movies sorted by rating",
    "Create Rating Histogram"
]

MIN_MOVIE_RATING = 0
MAX_MOVIE_RATING = 10

# This dictionary defines ANSI escape codes for text coloring in terminal output.
COLORS = {
    "RESET": '\033[0m',
    "RED": '\033[91m',
    "YELLOW": '\033[93m',
    "GREEN": '\033[92m',
    "CYAN": '\033[96m'
}


def print_error(error_message):
    """
    Prints error output in red color to the console

    Arguments:
        error_message (str): Error content printed out to the console
    """
    print(f"{COLORS['RED']}{error_message}{COLORS['RESET']}")


def get_colored_input(prompt):
    """
    Set distinct color for a prompt and input, collect and return user input

    Arguments:
         prompt: (str): The prompt

    Returns:
        Colored user input
    """
    user_input = input(f"{COLORS['GREEN']}{prompt}{COLORS['CYAN']}")
    print(f"{COLORS['RESET']}", end="")

    return user_input


def print_menu():
    """
    Prints the available menu items. Menu will be printed in distinct color
    """
    print(f"{COLORS['YELLOW']}\nMenu:")
    for count, item in enumerate(MENU_ITEMS):
        print(f"{count}. {item}")
    print(f"{COLORS['RESET']}")


def get_user_choice():
    """
    Prompts the user to select an option from the menu.

    Returns:
        int: The user's selected option as an integer if valid, otherwise None.
    """
    last_item_number = len(MENU_ITEMS)
    selected_number = int(get_colored_input(f"Enter choice (0-{last_item_number}): "))
    if 0 <= selected_number <= last_item_number:
        return selected_number
    return None


def print_movie(movies, movie_name):
    """
    Prints the movie name and its rating.

    Arguments:
        movie_name (str): The name of the movie.
        movies (dict): Source for lookup
    """
    movie = movies[movie_name]
    print(f"{movie_name} ({movie['year']}): {movie['rating']}")


def print_movies(movies):
    """
    Prints all movies and their properties in the provided dictionary.

    Arguments:
        movies (dict): Dictionary containing movie-rating entries.
    """
    print(f"{len(movies)} movies in total")
    for movie in movies:
        print_movie(movies, movie)


def get_valid_rating(min_rating=MIN_MOVIE_RATING, max_rating=MAX_MOVIE_RATING):
    """
    Prompts the user to input a valid movie rating within a specified range.

    Arguments:
        min_rating (int): Minimum allowed rating.
        max_rating (int): Maximum allowed rating.

    Returns:
        int: The validated rating entered by the user, or None if invalid.
    """
    user_rating = float(get_colored_input(f"Enter new movie rating: ({min_rating}-{max_rating}): "))
    if not min_rating <= user_rating <= max_rating:
        print_error(f"Rating {user_rating} is invalid")
        return None

    return user_rating


def add_movie():
    """Save new movie with its properties to 'movies.json' file"""
    user_movie = get_colored_input("Enter new movie name: ")
    user_year = int(get_colored_input("Enter new movie year: "))
    user_rating = get_valid_rating()
    if user_rating is None:
        return

    movies_storage.add_movie(user_movie, user_year, user_rating)
    print(f"Movie {user_movie} successfully added")


def get_valid_movie(message, movies):
    """
    Prompts the user to enter a valid movie name from the provided dictionary.

    Arguments:
        message (str): The message to display to the user.
        movies (dict): Dictionary of movies to validate against.

    Returns:
        str: The validated movie name, or None if the movie doesn't exist.
    """
    user_movie = get_colored_input(message)
    if user_movie not in movies:
        print_error(f"Movie {user_movie} does not exist!")
        return None

    return user_movie


def get_movie_ratings(movies):
    """
    Get ratings from movies dictionary and return it as a list

    Arguments:
        movies (dict): Dictionary from which the ratings will be read.

    Returns:
         list: The movie ratings for every movie in movies dict
    """
    return [m["rating"] for m in movies.values()]


def delete_movie(movies):
    """
    Deletes a movie from the provided movie dictionary.

    Arguments:
        movies (dict): Dictionary from which the movie will be deleted.
    """
    deleted_movie = get_valid_movie("Enter movie name to delete: ", movies)
    if deleted_movie is None:
        return

    del movies[deleted_movie]
    print("Movie successfully deleted")


def update_movie(movies):
    """
    Updates the rating of an existing movie in the provided movie dictionary.

    Arguments:
        movies (dict): Dictionary containing movies and their ratings.
    """
    updated_movie = get_valid_movie("Enter movie name: ", movies)
    if updated_movie is None:
        return

    updated_rating = get_valid_rating()
    if updated_rating is None:
        return

    movies[updated_movie]["rating"] = updated_rating
    print(f"Movie {updated_movie} successfully updated")


def print_statistics(movies):
    """
    Prints statistical information about movies:
        - average and median movie rating
        - highest and lowest-rated movies

    Arguments:
        movies (dict): Dictionary containing movies and their ratings.
    """
    ratings = get_movie_ratings(movies)
    avg_rating = statistics.mean(ratings)
    median_rating = statistics.median(ratings)

    highest_rated_movie = max(movies, key=lambda movie: movies[movie]["rating"])
    lowest_rated_movie = min(movies, key=lambda movie: movies[movie]["rating"])

    print(f"Average rating: {avg_rating}")
    print(f"Median rating: {median_rating}")
    print(f"Best movie: {highest_rated_movie}")
    print(f"Worst movie: {lowest_rated_movie}")


def print_random_movie(movies):
    """
    Selects and prints a random movie from the movie dictionary.

    Arguments:
        movies (dict): Dictionary containing movies and their ratings.
    """
    movie_list = list(movies.keys())
    random_movie = random.choice(movie_list)
    random_rating = movies[random_movie]["rating"]

    print(f"Your movie for tonight: {random_movie}, it's rated: {random_rating}")


def fuzzy_search_movie(search_term, movies, close_word_matches_max=2, cutoff=0.7):
    """
    Performs a fuzzy search on a list of movie titles to find approximate
    matches in movie words based on a search term.

    Arguments:
        search_term (str): The partial movie title to search for.
        movies (dict): A dictionary containing movie-rating key-value pairs.
        close_word_matches_max (int, optional):
            The maximum of close word matches found in movie title. Defaults to 2.
        cutoff (float, optional): A threshold value between 0 and 1,
        representing how close a match should be to search term. Defaults to 0.7.
    """
    normalized_search_term = get_normalized_text(search_term)
    write_search_info = True

    for movie in movies:
        normalized_movie_title = get_normalized_text(movie)
        # compare each word of movie with search term
        # return up to 'n' closest matching words
        close_matches_count = len(get_close_matches(normalized_search_term,
                                                    normalized_movie_title.split(),
                                                    n=close_word_matches_max, cutoff=cutoff))
        # print movie with at least one search matching word found in its title
        if close_matches_count > 0:
            if write_search_info:
                print_error(f"The movie {search_term} does not exist. Did you mean:")
                write_search_info = False

            print(movie)

    if write_search_info:
        print_error(f"No movie named {search_term} was found")


def get_normalized_text(text):
    """
    Normalizes text by trimming whitespace, making it case-insensitive, and removing accents.

    Arguments:
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


def search_movie(movies):
    """
    Performs case-insensitive partial search in movies and prints matching entries.

    Arguments:
        movies (dict): Dictionary containing movies and their ratings.
    """
    search_term = get_colored_input("Enter part of movie name: ")
    search_term_lower = get_normalized_text(search_term)
    match_found = False
    for movie, movie_data in movies.items():
        if search_term_lower in get_normalized_text(movie):
            print(f"{movie}, {movie_data['rating']}")
            match_found = True

    if not match_found:
        fuzzy_search_movie(search_term, movies)


def sort_movies_by_rating(movies, reverse=True):
    """
    Sorts movies by rating in descending order by default and prints them.

    Arguments:
        movies (dict): Dictionary containing movies and their ratings.
        reverse (bool): If True, sorts in descending order, otherwise ascending.
    """
    sorted_movies = dict(
        sorted(movies.items(), key=lambda item: item[1]["rating"], reverse=reverse)
    )

    for movie in sorted_movies:
        print_movie(movies, movie)


def create_rating_histogram(movies):
    """
    Generates and saves a histogram of movie ratings from a dictionary of movies.

    Arguments:
        movies (dict): A dictionary where keys are movie titles and values are ratings (numeric).

    Displays:
        Prompts the user to enter a filename to save the histogram as a PNG image.

    Raises:
        Prints an error message if the filename is invalid or contains restricted characters.
    """
    ratings = get_movie_ratings(movies)

    # create histogram
    plt.hist(ratings)

    # Adding labels and title
    plt.xlabel('Rating')
    plt.ylabel('Frequency (count of movies)')
    plt.title('Distribution of movie ratings')

    user_filename = get_colored_input("Enter filename for saving histogram: ")

    invalid_chars = r'[<>:"/\\|?*]'
    if user_filename == "" or re.search(invalid_chars, user_filename):
        print_error("Invalid filename")
        return

    # save figure to the file and release resources
    plt.savefig(f"{user_filename}.png")
    plt.close()


def execute_task(user_choice, movies):
    """
    Executes a task based on the user's menu choice.

    Arguments:
        user_choice (int): The option selected by the user.
        movies (dict): Dictionary containing movies and their ratings.

    Returns:
        bool: True if the task was successfully completed, False otherwise.
    """
    if user_choice is None:
        print_error("Invalid choice")
        return False

    print()

    if user_choice == 0:
        sys.exit("Bye!")
    elif user_choice == 1:
        print_movies(movies)
    elif user_choice == 2:
        add_movie()
    elif user_choice == 3:
        delete_movie(movies)
    elif user_choice == 4:
        update_movie(movies)
    elif user_choice == 5:
        print_statistics(movies)
    elif user_choice == 6:
        print_random_movie(movies)
    elif user_choice == 7:
        search_movie(movies)
    elif user_choice == 8:
        sort_movies_by_rating(movies)
    elif user_choice == 9:
        create_rating_histogram(movies)

    print()

    return True


def wait_for_user_action():
    """
    Halts program execution, prompting the user to press Enter to continue.
    """
    get_colored_input("Press enter to continue")


def main():
    """Main function to run the program."""
    movies = movies_storage.get_movies()

    print("********** My Movies Database **********")

    try:
        while True:
            print_menu()

            user_choice = get_user_choice()
            task_is_completed = execute_task(user_choice, movies)

            if task_is_completed:
                wait_for_user_action()
    finally:
        # Reset output color upon expected or unexpected exit
        print(COLORS['RESET'], end="")


if __name__ == "__main__":
    main()
