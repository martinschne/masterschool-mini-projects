import json
import os

from .istorage import IStorage


class StorageJson(IStorage):
    """
    Persistent storage for accessing and saving data in JSON format.

    This class provides methods to interact with a JSON file, enabling
    reading, writing, and maintaining a database of movies.
    """

    def __init__(self, file_path):
        """
        Initialize the StorageJson object with a specified file path.

        This method sets up the storage file path, creates a new JSON file
        if it doesn't already exist, and ensures that the directory for
        storing data is valid.

        Args:
            file_path (str): The name of the JSON file to use for storage.

        Raises:
            OSError: If creating the JSON file fails due to file system
            issues.

        Side Effects:
            - Creates a new JSON file at the specified path if it does not
              exist.
            - Prints a message indicating whether the file was created or
              an error occurred.
        """
        current_dir = os.getcwd()
        self._file_path = os.path.join(current_dir, IStorage.data_dir, file_path)
        if not os.path.exists(self._file_path):
            try:
                self._save_movies({})
                print(f"New json file was created at path: '{self._file_path}'.")
            except OSError:
                print(f"Error: creating json file at path: '{self._file_path}' failed.")

    def _save_movies(self, movies: dict):
        """
        Save all movie data to the JSON file.

        This method takes a dictionary containing all movie data and writes
        it to the JSON file, overwriting any existing content.

        Args:
            movies (dict): A dictionary containing movie data to save.
            For example:
            {
                "Titanic": {
                    "rating": 9,
                    "year": 1999
                },
                "Inception": {
                    "rating": 8.8,
                    "year": 2010
                }
            }

        Raises:
            IOError: If saving to the JSON file fails due to file system
            issues.
        """
        with open(self._file_path, 'w') as json_file_obj:
            json_file_obj.write(json.dumps(movies))

    def list_movies(self):
        """
        Retrieve all movies from the database.

        This method loads movie information from the JSON file and returns
        it as a dictionary of dictionaries, where each movie title is a key
        and its associated details (e.g., rating, year) are stored in a
        nested dictionary.

        Returns:
            dict: A dictionary containing movie information. For example:
            {
                "Titanic": {
                    "rating": 9,
                    "year": 1999
                },
                "Inception": {
                    "rating": 8.8,
                    "year": 2010
                }
            }
        """
        with open(self._file_path, 'r') as json_file_obj:
            movies = json.loads(json_file_obj.read())

        return movies

    def add_movie(self, title, year, rating):
        """
        Add a new movie to the database.

        This method retrieves all movies from the storage, adds a new movie
        with the provided details, and saves the updated list back to the
        database.

        Args:
            title (str): The title of the movie to add.
            year (int): The release year of the movie.
            rating (float): The rating of the movie.
            poster (str): The URL of the movie's poster image.
        """
        movies = self.list_movies()
        movies[title] = {
            "rating": rating,
            "year": year
        }

        self._save_movies(movies)

    def delete_movie(self, title: str):
        """
        Delete a movie from the database.

        This method retrieves all movies from the storage, deletes the
        specified movie by its title, and saves the updated list back to
        the database.

        Args:
            title (str): The title of the movie to delete.
        """
        movies = self.list_movies()
        del movies[title]

        self._save_movies(movies)

    def update_movie(self, title, rating):
        """
        Update the rating of a movie in the database.

        This method retrieves all movies from the storage, updates the
        rating of the specified movie, and saves the changes back to the
        database.

        Args:
            title (str): The title of the movie to update.
            rating (float): The new rating to assign to the movie.
        """
        movies = self.list_movies()
        movies[title]["rating"] = rating

        self._save_movies(movies)

    def is_movie_in_storage(self, title):
        """
        Checks if a movie with the given title exists in the storage.

        Args:
            title (str): The title of the movie to check.

        Returns:
            bool: True if the movie exists in the storage, False otherwise.
        """
        movies = self.list_movies()
        movies_keys = [key.lower() for key in movies.keys()]
        return title.lower() in movies_keys

# Sanity check:
# storage = StorageJson("movies.json")
# storage.add_movie("Hello", 1988, 3, "me")
# print(storage.list_movies())
# storage.add_movie("Bye", 1991, 10, "me")
# print(storage.list_movies())
# storage.update_movie("Hello", 0)
# storage.update_movie("Bye", 0)
# print(storage.list_movies())
# print(f"Hello in storage: {storage.is_movie_in_storage("Hello")}")
# print(f"Naomi in storage: {storage.is_movie_in_storage("Naomi")}")
#
# print(f"Bye in storage: {storage.is_movie_in_storage("Bye")}")
# storage.delete_movie("Bye")
# print(f"Bye in storage: {storage.is_movie_in_storage("Bye")}")
# print(storage.list_movies())
