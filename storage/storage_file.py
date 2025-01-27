from storage.istorage import IStorage


class StorageFile(IStorage):
    """
    Base class for file storage implementation. Shares blueprint with
    common method implementations and methods to override in subclasses.
    """
    data_dir = "data"

    def _save_movies(self, movies: dict):
        raise NotImplementedError("Subclasses must implement '_save_movies'.")

    def list_movies(self):
        raise NotImplementedError("Subclasses must implement 'list_movies'.")

    def add_movie(self, title: str, year: int, rating: float):
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

    def update_movie(self, title: str, rating: float):
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

    def is_movie_in_storage(self, title: str):
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
