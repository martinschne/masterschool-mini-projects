import csv
import os

from utils import convert_to_number, validate_url
from .storage_file import StorageFile


class StorageCsv(StorageFile):
    """
    Persistent storage for accessing and saving data in CSV format.

    This class provides methods to interact with a CSV file, enabling
    reading, writing, and maintaining a database of movies.
    """

    fieldnames = ["title", "rating", "year", "poster_url", "notes"]

    def __init__(self, file_path: str):
        """
        Initialize the StorageCsv object with a specified file path.

        This method sets up the storage file path, creates a new CSV file
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
                print(f"New csv file was created at path: '{self._file_path}'.")
            except OSError:
                print(f"Error: creating csv file at path: '{self._file_path}' failed.")

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
            IOError: If saving to the CSV file fails due to file system
            issues.
        """
        with open(self._file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, StorageCsv.fieldnames)
            writer.writeheader()
            for movie in movies:
                title = movie
                rating = movies[movie]["rating"]
                year = movies[movie]["year"]
                poster_url = movies[movie]["poster_url"]
                notes = movies[movie]["notes"]
                writer.writerow({
                    "title": title,
                    "rating": rating,
                    "year": year,
                    "poster_url": poster_url,
                    "notes": notes
                })

    def list_movies(self):
        """
        Retrieve all movies from the database.

        This method loads movie information from the CSV file and returns
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
        movies = {}
        with open(self._file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # save the record to movies in desired format
                movies[row["title"]] = {
                    "rating": convert_to_number(row["rating"], float),
                    "year": convert_to_number(row["year"], int),
                    "poster_url": validate_url(row["poster_url"]),
                    "notes": row["notes"]
                }

        return movies
