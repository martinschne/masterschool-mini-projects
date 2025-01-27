from storage import IStorage
from utils import COLORS, get_colored_input, wait_for_user_action, print_error, reset_output_color
from project import CommandHandler


class MovieApp:
    _instance = None

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
        "Movies sorted by year",
        "Filter movies by year/rating",
        "Create Rating Histogram"
    ]

    def __new__(cls, storage: IStorage):
        """
        Instantiates the MovieApp class only once in the lifetime of the program.
        Subsequent instantiations will return the same instance. (Singleton)

        Args:
            storage: (IStorage) storage implementation.
        """
        if not cls._instance:
            cls._instance = super(MovieApp, cls).__new__(cls)
            cls._instance.__storage = storage
        return cls._instance

    def __init__(self, storage: IStorage):
        self.__storage = storage
        self.__command_handler = CommandHandler(storage)

    def _print_menu(self):
        """Prints the available menu items in distinct color."""
        print(f"{COLORS['YELLOW']}\nMenu:")
        for count, item in enumerate(MovieApp.MENU_ITEMS):
            print(f"{count}. {item}")
        print(f"{COLORS['RESET']}")

    def _get_user_choice(self):
        """
        Prompts the user to select an option from the menu.

        Returns:
            (int): The user's selected option as an integer if valid, otherwise None.
        """
        last_item_number = len(MovieApp.MENU_ITEMS) - 1
        selected_number = int(get_colored_input(f"Enter choice (0-{last_item_number}): "))
        if 0 <= selected_number <= last_item_number:
            return selected_number
        return None

    def _generate_website(self, par):
        pass

    def run(self):
        """
        Runs the main application loop for the Movies Theater program.

        This method handles the following responsibilities:
        - Displays the main menu to the user.
        - Captures and validates user input for menu choices.
        - Delegates commands to the command handler for execution.
        - Provides user feedback and waits for user action after tasks are completed.

        The method continuously runs until interrupted by the user or an unexpected event.
        It ensures the output color is reset before exiting.

        Raises:
            ValueError: If the user's input for menu selection is invalid.
        """
        movies = self.__storage.list_movies()

        print("********** My Movies Database **********")

        try:
            while True:
                self._print_menu()
                try:
                    user_choice = self._get_user_choice()
                    if user_choice is None:
                        raise ValueError
                except ValueError:
                    print_error("Invalid choice, please try again.\n")
                    wait_for_user_action()
                    continue
                task_is_completed = self.__command_handler.execute_command(user_choice, movies)

                if task_is_completed:
                    wait_for_user_action()
        finally:
            # Reset output color upon expected or unexpected exit
            reset_output_color()
