import argparse
import sys

from project import MovieApp
from storage import StorageJson, StorageCsv
from utils import print_error


def parse_args():
    """
    Parses command-line arguments and initializes the appropriate storage class.

    This function reads the `filename` argument from the command line, determines
    whether it is a JSON or CSV file, and initializes the corresponding storage
    class (`StorageJson` or `StorageCsv`). If the file extension is invalid, it
    prints an error message and exits the program.

    Returns:
        StorageJson | StorageCsv: An instance of the appropriate storage class.

    Example:
        >>> python main.py movies.json
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("filename",
                        help="File for saving movie data. Supported formats: json, csv. Example: 'file.json'")
    args = parser.parse_args()

    storage_file: str = args.filename
    if storage_file.endswith(".json"):
        storage = StorageJson(storage_file)
    elif storage_file.endswith(".csv"):
        storage = StorageCsv(storage_file)
    else:
        print_error("Error: Invalid filename provided! File must have a .json or .csv extension.")
        sys.exit("Exiting!")

    return storage


def main():
    """Main function to run the program."""
    storage_obj = parse_args()
    movie_app = MovieApp(storage_obj)
    movie_app.run()


if __name__ == "__main__":
    main()
