import json
import os
import random
import re
import statistics
import sys
from difflib import get_close_matches
from urllib.parse import urlencode, urljoin

# pylint: disable=import-error
import matplotlib
import matplotlib.pyplot as plt
import requests
from dotenv import load_dotenv

from storage import IStorage
from utils import (
    get_title_from_user,
    get_year_from_user,
    get_rating_from_user,
    get_colored_input,
    get_answer_from_user,
    get_normalized_input,
    print_error,
    convert_to_number,
    validate_url,
    get_notes_from_user
)

# Use the Agg backend for rendering to a file
matplotlib.use('Agg')

load_dotenv()

API_KEY = os.getenv("API_KEY")

class CommandHandler:

    RATING_KEY = "rating"
    YEAR_KEY = "year"
    POSTER_URL_KEY = "poster_url"
    NOTES_KEY = "notes"

    def __init__(self, storage: IStorage):
        """
        Initialize the CommandHandler with a storage dependency.

        Args:
            storage (IStorage): An object responsible for data storage implementation
        """
        self._storage = storage

    def _print_movie(self, movies: dict, movie_name: str):
        """
        Prints the movie name and its rating.
    
        Args:
            movie_name (str): name of the movie
            movies (dict): lookup source
        """
        movie_data = movies[movie_name]
        year = movie_data["year"]
        rating = movie_data["rating"]
        movie_year = "N/A" if year is None else year
        movie_rating = "N/A" if rating is None else rating

        print(f"{movie_name} ({movie_year}): {movie_rating}")

    def _command_print_movies(self, movies: dict):
        """
        Prints all movies and their properties in the provided dictionary.
    
        Args:
            movies (dict): Dictionary containing movie - movie data (year/rating) entries.
        """
        print(f"{len(movies)} movies in total")
        for movie in movies:
            self._print_movie(movies, movie)

    def _load_movie(self, title: str) -> tuple[str | None, dict | None]:
        found_movie_title, found_movie_data = None, None

        base_url = "https://www.omdbapi.com/"
        params = {"apikey": API_KEY, "t": title, "type": "movie"}

        try:
            response = requests.get(url=urljoin(base_url, "?" + urlencode(params)))
        except ConnectionError:
            print_error("Error: Connecting to the omdb server failed, please try again later.")
            return None, None

        response_obj = json.loads(response.text)

        if response.status_code == 200:
            movie_was_found = eval(response_obj["Response"])

            if movie_was_found:
                new_title = response_obj["Title"]
                new_year = convert_to_number(response_obj["Year"], int)
                new_rating = convert_to_number(response_obj["imdbRating"], float)
                new_poster_url = validate_url(response_obj["Poster"])

                new_movie_data = {
                    CommandHandler.YEAR_KEY: new_year,
                    CommandHandler.RATING_KEY: new_rating,
                    CommandHandler.POSTER_URL_KEY: new_poster_url
                }

                found_movie_title, found_movie_data = new_title, new_movie_data
            else:
                print(response_obj["Error"])
        else:
            print_error("Error: Accessing movie data failed, please try again later.")

        return found_movie_title, found_movie_data

    def _command_add_movie(self) -> tuple[str | None, dict | None]:
        """
            Saves new movie with its properties to 'movies.json' file.
    
            Returns:
                user_movie (str) and user_movie_data (dict) as a tuple
                if movie was successfully found and fetched from omdb api
                otherwise user_movie_data will be None.
        """
        title_from_user = get_title_from_user()
        found_movie_title, found_movie_data = self._load_movie(title_from_user)

        if found_movie_title is not None:
            if self._storage.is_movie_in_storage(found_movie_title):
                print_error("Movie is already in the storage.")
                return None, None

            # save the movie
            year = found_movie_data[CommandHandler.YEAR_KEY]
            rating = found_movie_data[CommandHandler.RATING_KEY]
            poster = found_movie_data[CommandHandler.POSTER_URL_KEY]

            self._storage.add_movie(found_movie_title, year, rating, poster)
            print(f"Movie '{found_movie_title}' was successfully added.")

        return found_movie_title, found_movie_data

    def _get_existing_movie(self, message: str, movies: dict) -> str:
        """
        Prompts the user to enter a valid movie name from the provided dictionary.
        Repeats prompts until valid movie was entered (existing movie title).
    
        Args:
            message (str): The message to display to the user.
            movies (dict): Dictionary of movies to validate against.
    
        Returns:
            str: The validated movie name.
        """
        trials = 3
        while trials != 0:
            user_movie = get_title_from_user(message)
            if user_movie in movies:
                return user_movie
            else:
                print_error(f"Movie {user_movie} does not exist!")
                trials -= 1

        print("Tip: list all movies to see available movies.")
        return None

    def _get_movie_ratings(self, movies: dict) -> list[float]:
        """
        Get ratings from movies dictionary and return it as a list.
    
        Args:
            movies (dict): Dictionary from which the ratings will be read.
    
        Returns:
             list: The movie ratings for every movie in movies dict.
        """
        return [m[CommandHandler.RATING_KEY] for m in movies.values() if m[CommandHandler.RATING_KEY] is not None]

    def _command_delete_movie(self, movies: dict) -> str:
        """
        Get movie name from user input, validate its existence in loaded 'movies' dict
        and delete the movie from stored data.
    
        Args:
            movies (dict): Loaded movie data for validation against user input.
    
        Returns:
            deleted_movie (str): Movie title that was deleted.
        """
        deleted_movie = self._get_existing_movie("Enter movie name to delete: ", movies)

        if deleted_movie is not None:
            self._storage.delete_movie(deleted_movie)
            print("Movie successfully deleted")

        return deleted_movie

    def _command_update_movie(self, movies: dict) -> tuple[str, float]:
        """
        Updates the notes of an existing movie in the provided movie dictionary.
        Repeatedly prompts the user until valid movie and notes are entered.
    
        Args:
            movies (dict): Dictionary containing movies and their data (years/ratings).
    
        Returns:
            Tuple of: updated_movie (str) and new_notes (str).
        """
        updated_movie = self._get_existing_movie("Enter movie name: ", movies)
        new_notes = None

        if updated_movie is not None:
            new_notes = get_notes_from_user()

            self._storage.update_movie(updated_movie, new_notes)
            print(f"Movie {updated_movie} successfully updated")

        return updated_movie, new_notes

    def _get_movies_with_property(self, property: str, movies: dict):
        filtered_movies = {movie: movie_data for movie, movie_data in movies.items() if
                           movie_data[property] is not None}
        return filtered_movies

    def _command_print_statistics(self, movies: dict):
        """
        Prints statistical information about movies:
            - average and median movie rating
            - highest and lowest-rated movie
    
        Args:
            movies (dict): Dictionary containing movies and their data (years/ratings).
        """
        ratings = self._get_movie_ratings(movies)
        avg_rating = statistics.mean(ratings)
        median_rating = statistics.median(ratings)

        rated_movies = self._get_movies_with_property(CommandHandler.RATING_KEY, movies)
        highest_rated_movie = max(rated_movies, key=lambda movie: movies[movie][CommandHandler.RATING_KEY])
        lowest_rated_movie = min(rated_movies, key=lambda movie: movies[movie][CommandHandler.RATING_KEY])

        print(f"Average rating: {avg_rating:.1f}")
        print(f"Median rating: {median_rating:.1f}")
        print(f"Best movie: {highest_rated_movie}")
        print(f"Worst movie: {lowest_rated_movie}")

    def _command_print_random_movie(self, movies: dict):
        """
        Selects and prints a random movie from the movie dictionary.
    
        Args:
            movies (dict): Dictionary containing movies and their data (years/ratings).
        """
        movie_list = list(movies.keys())
        random_movie = random.choice(movie_list)
        random_rating = movies[random_movie][CommandHandler.RATING_KEY]

        print(f"Your movie for tonight: {random_movie}, it's rated: {random_rating}")

    def _fuzzy_search_movie(
            self,
            search_term: str,
            movies: dict,
            close_word_matches_max: int = 2,
            cutoff: float = 0.7):
        """
        Performs a fuzzy search on a list of movie titles to find approximate
        matches in movie words based on a search term.
    
        Args:
            search_term (str): The partial movie title to search for.
            movies (dict): A dictionary containing movies and their data (years/ratings).
            close_word_matches_max (int, optional):
                The maximum of close word matches found in movie title. Defaults to 2.
            cutoff (float, optional): A threshold value between 0 and 1,
            representing how close a match should be to search term. Defaults to 0.7.
        """
        normalized_search_term = get_normalized_input(search_term)
        write_search_info = True

        for movie in movies:
            normalized_movie_title = get_normalized_input(movie)
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

    def _command_search_movie(self, movies: dict):
        """
        Performs case-insensitive partial search in movies and prints matching entries.
    

        Args:
            movies (dict): Dictionary containing movies and their data (years/ratings).
        """
        search_term = get_title_from_user("Enter part of movie name: ")
        search_term_lower = get_normalized_input(search_term)
        match_found = False
        for movie, movie_data in movies.items():
            if search_term_lower in get_normalized_input(movie):
                self._print_movie(movies, movie)
                match_found = True

        if not match_found:
            self._fuzzy_search_movie(search_term, movies)

    def _command_sort_movies(self, movies: dict, sort_by: str, reverse: bool = True):
        """
        Sorts movies by rating in descending order by default and prints them.
    
        Args:
            movies (dict): Dictionary containing movies and their data (years/ratings).
            sort_by (str): Sort according to the movie data property, e.g.: 'rating', 'year'.
            reverse (bool): If True, sorts in descending order, otherwise ascending.
        """
        if sort_by == CommandHandler.YEAR_KEY:
            reverse = get_answer_from_user(
                "Do you want to see the latest movies first? (yes/no): "
            )

        sortable_movies = dict(
            sorted(
                self._get_movies_with_property(sort_by, movies).items(),
                key=lambda item: item[1][sort_by],
                reverse=reverse
            )
        )

        for movie in sortable_movies:
            self._print_movie(sortable_movies, movie)

        unsortable_movies = {title: movie_data for title, movie_data in movies.items() if
                             (title, movie_data) not in sortable_movies.items()}

        if unsortable_movies:
            print(f"\nThese movies could not be sorted by '{sort_by}':")
            for movie in unsortable_movies:
                self._print_movie(unsortable_movies, movie)

    def _command_filter_movies(self, movies: dict):
        """
        Asks the user for optional filtering parameters: minimal rating, start year, end year.
        Prints only movies matching the parameter boundaries for year or rating entered by user.
        """
        min_rating = get_rating_from_user(
            prompt="Enter minimum rating (leave blank for no minimum rating): ",
            allow_empty_input=True
        )
        min_year = get_year_from_user(
            prompt="Enter start year (leave blank for no start year): ",
            allow_empty_input=True
        )
        max_year = get_year_from_user(
            prompt="Enter end year (leave blank for no end year): ",
            allow_empty_input=True
        )
        movies_filtered = 0
        for movie in movies:
            conditions_met = []

            movie_rating = movies[movie][CommandHandler.RATING_KEY]
            movie_year = movies[movie][CommandHandler.YEAR_KEY]

            if not min_rating == "" and movie_rating is not None:
                conditions_met.append(movie_rating >= min_rating)

            if not min_year == "" and movie_year is not None:
                conditions_met.append(movie_year >= min_year)

            if not max_year == "" and movie_year is not None:
                conditions_met.append(movie_year <= max_year)

            if all(conditions_met):
                movies_filtered += 1
                self._print_movie(movies, movie)

        if movies_filtered == 0:
            print_error("No movies matched the filtering criteria.")

    def _command_create_rating_histogram(self, movies: dict):
        """
        Generates and saves a histogram of movie ratings from a dictionary of movies.
    
        Args:
            movies (dict): Dictionary containing movies and their data (years/ratings).
    
        Displays:
            Prompts the user to enter a filename to save the histogram as a PNG image.
    
        Raises:
            Prints an error message if the filename is invalid or contains restricted characters.
        """
        ratings = self._get_movie_ratings(movies)

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

    def _load_template_page(self, page_filename: str):
        """Reads the content of a file and returns it as a string."""
        static_dir = "_static"
        with open(os.path.join(static_dir, page_filename), "r", encoding="utf-8") as file:
            return file.read()

    def save_generated_page(self, content: str, page_filename="index.html"):
        output_dir = "_static"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, page_filename)

        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

        print(f"Page saved at: {file_path}")

    def _command_generate_page(self, movies: dict):
        """
        Generates a html file according to the template.

        Args:
            movies (dict): Dictionary containing movies and their data (years/ratings).
        """
        try:
            html_template = self._load_template_page("index_template.html")
        except FileNotFoundError:
            print_error("Error: Html template is missing. Unable to generate the website.")
            return
        except IOError:
            print_error("Error: Could not read the template file. Unable to generate the website.")
            return

        movie_grid_output = ""
        for title, movie_data in movies.items():
            movie_poster = movie_data.get("poster_url", "https://placehold.co/128x193/?text=No%0Aposter")
            movie_year = movie_data.get("year")
            movie_notes = movie_data.get("notes")
            movie_rating = movie_data.get("rating")
            movie_grid_output += f"""<div class="movie">
            <img class="movie-poster" title="{movie_notes or ""}"
                 src="{movie_poster or "https://placehold.co/128x193/?text=No%0APoster"}"
                 alt="{title} - movie poster" />
            <div class="movie-rating">&#x2B50; {movie_rating or "-"}&nbsp;&nbsp;&nbsp;</div>
            <div class="movie-title">{title}</div>
            <div class="movie-year">{movie_year or ""}</div>
        </div>
        """

        html_template = html_template.replace("__TEMPLATE_TITLE__", "My Movie App")
        html_template = html_template.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_output.rstrip())

        try:
            self.save_generated_page(html_template)
            print("Website was successfully generated.")
        except Exception as e:
            print_error("Error: generating website failed!\n", e)

    def execute_command(self, user_choice: int, movies: dict) -> bool:
        """
        Executes a task based on the user's menu choice.

        Args:
            user_choice (int): The option selected by the user.
            movies (dict): Dictionary containing movies and their data (years/ratings).

        Returns:
            bool: True if the task was successfully completed, False otherwise.
        Note:
            Task functions add/delete/update bellow cause direct side effect:
            updating 'movies' dictionary.
            This approach avoids introducing side effects in more functions,
            namely those that are mutating the data:
                add_movie
                delete_movie
                update_movie
            and saves expensive read operations on stored data.
        """
        if user_choice is None:
            print_error("Invalid choice")
            return False

        print()

        if not movies and user_choice != 0 and user_choice != 2:
            print_error("No movies were found. Try adding some first.\n")
            return True

        if user_choice == 0:
            sys.exit("Bye!")
        elif user_choice == 1:
            self._command_print_movies(movies)
        elif user_choice == 2:
            new_movie, new_movie_data = self._command_add_movie()
            if new_movie_data is not None:
                movies[new_movie] = new_movie_data
        elif user_choice == 3:
            deleted_movie = self._command_delete_movie(movies)
            if deleted_movie is not None:
                movies.pop(deleted_movie, None)
        elif user_choice == 4:
            updated_movie, new_notes = self._command_update_movie(movies)
            if updated_movie is not None:
                movies[updated_movie][CommandHandler.NOTES_KEY] = new_notes
        elif user_choice == 5:
            self._command_print_statistics(movies)
        elif user_choice == 6:
            self._command_print_random_movie(movies)
        elif user_choice == 7:
            self._command_search_movie(movies)
        elif user_choice == 8:
            self._command_sort_movies(movies, CommandHandler.RATING_KEY)
        elif user_choice == 9:
            self._command_sort_movies(movies, CommandHandler.YEAR_KEY)
        elif user_choice == 10:
            self._command_filter_movies(movies)
        elif user_choice == 11:
            self._command_create_rating_histogram(movies)
        elif user_choice == 12:
            self._command_generate_page(movies)

        print()

        return True
