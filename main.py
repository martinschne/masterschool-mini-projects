from project import MovieApp
from storage import StorageJson


def main():
    """Main function to run the program."""
    storage = StorageJson("movies.json")
    movie_app = MovieApp(storage)
    movie_app.run()


if __name__ == "__main__":
    main()
