import sys

from products import Product, NonStockedProduct, LimitedProduct
from promotions import SecondHalfPrice, ThirdOneFree, PercentDiscount
from store import Store


def print_store_products(store: Store):
    """
    Prints a numbered list of all products in the store with their details.

    :param store: Store object exposing its products for displaying.
    :type store: Store
    """
    print("------")
    for index, product in enumerate(store.get_all_products()):
        print(f"{index + 1}. {product}")
    print("------")


def print_store_items_amount(store: Store):
    """
    Prints the total quantity of all items assigned to the store instance.

    :param store: Store object exposing its products for item counting.
    :type store: Store
    """
    print(f"Total of {store.get_total_quantity()} items in store")


def make_order(store: Store):
    """
    Navigates the user through the order creation process.

    Steps:
    - Display the products available in the store.
    - Repeatedly prompt the user to add a new item consisting of a
      Product instance and ordered quantity to the shopping list.
    - Finalize the order creation when the user provides empty input.

    :param store: Store object exposing its methods for managing ordered products it contains.
    :type store: Store
    """
    shopping_list = []

    print_store_products(store)
    print("When you want to finish order, enter empty text.")

    while True:
        selected_product_index = input("Which product # do you want? ")
        quantity = input("What amount do you want? ")

        if selected_product_index == "" or quantity == "":
            break

        try:
            product_index = int(selected_product_index) - 1
            product = store.get_all_products()[product_index]
            quantity = int(quantity)

            item = (product, quantity)
            shopping_list.append(item)
            print("Product added to list!\n")
        except (ValueError, IndexError):
            print("Error adding product!\n")

    if len(shopping_list) > 0:
        try:
            total_order = store.order(shopping_list)
            if total_order != 0:
                print("********")
                print(f"Order made! Total payment: ${total_order}")
        except ValueError as e:
            print(e)


def start(store: Store):
    """
    Provides a terminal user interface to the user.

    Handles menu printing, item selection, and execution of the corresponding
    helper function referenced in the `menu_options` list.

    :param store: Store object for exposing store methods to helper functions.
    :type store: Store
    """
    menu_options = [
        lambda: print_store_products(store),
        lambda: print_store_items_amount(store),
        lambda: make_order(store),
        sys.exit
    ]

    while True:
        print("   Store Menu")
        print("   ----------")
        print("1. List all products in store")
        print("2. Show total amount in store")
        print("3. Make an order")
        print("4. Quit")

        try:
            user_choice = int(input("Please choose a number: "))
            menu_index = user_choice - 1

            if 0 <= menu_index < len(menu_options):
                menu_options[user_choice - 1]()
        except ValueError:
            print("Error with your choice! Try again!")
        except KeyboardInterrupt:
            return

        print()


def main():
    """
    Main method to start the program.

    Sets up the initial stock of inventory, promotions, and starts the store.
    """
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    ]

    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half price!")
    third_one_free = ThirdOneFree("Third One Free!")
    thirty_percent = PercentDiscount("30% off!", percent=30)

    # Add promotions to products
    product_list[0].promotion = second_half_price
    product_list[1].promotion = third_one_free
    product_list[3].promotion = thirty_percent

    best_buy = Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
