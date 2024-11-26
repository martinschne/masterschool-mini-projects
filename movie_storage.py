import json
import os.path

DATA_DIR = "data"
MOVIES_JSON = "movies.json"


get_movies_path = lambda: os.path.join(DATA_DIR, MOVIES_JSON)


def get_movies():
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data.

    For example, the function may return:
    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open(get_movies_path(), 'r') as json_file_obj:
        movies = json.loads(json_file_obj.read())

    return movies

def save_movies(movies):
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open(get_movies_path(), 'w') as json_file_obj:
        json_file_obj.write(json.dumps(movies))


def add_movie(title, year, rating):
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title] = {
        "year": year,
        "rating": rating
    }

    save_movies(movies)


def delete_movie(title):
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    del movies[title]

    save_movies(movies)


def update_movie(title, rating):
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies()
    movies[title]["rating"] = rating

    save_movies(movies)
