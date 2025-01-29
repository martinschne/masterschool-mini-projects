import json
import os

from .storage_file import StorageFile

print(f"Running {__file__} as {'__main__' if __name__ == '__main__' else 'imported module'}.")


class StorageJson(StorageFile):
    """
    Persistent storage for accessing and saving data in JSON format.

    This class provides methods to interact with a JSON file, enabling
    reading, writing, and maintaining a database of movies.
    """

    def __init__(self, file_path: str):
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
        self._file_path = os.path.join(current_dir, StorageFile.data_dir, file_path)
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
                    "year": 1999,
                    "poster_url": "https://example_movie.com/",
                    "notes": "Very good movie..."
                },
                "Inception": {
                    "rating": 8.8,
                    "year": 2010,
                    "poster_url": "https://example_movie2.com/",
                    "notes": None
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
                    "year": 1999,
                    "poster_url": "https://example_movie.com/",
                    "notes": "Very good movie..."
                },
                "Inception": {
                    "rating": 8.8,
                    "year": 2010,
                    "poster_url": "https://example_movie2.com/",
                    "notes": None
                }
            }
        """
        with open(self._file_path, 'r') as json_file_obj:
            movies = json.loads(json_file_obj.read())

        return movies