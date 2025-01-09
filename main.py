import sys

from products import Product
from store import Store


def print_store_products(store: Store):
    print("------")
    for index, product in enumerate(store.get_all_products()):
        print(f"{index + 1}. {product.show()}")
    print("------")


def print_store_items_amount(store: Store):
    print(f"Total of {store.get_total_quantity()} items in store")


def make_order(store: Store):
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
        print("********")
        print(f"Order made! Total payment: ${store.order(shopping_list)}")


def start(store: Store):
    menu_options = [
        lambda: print_store_products(store),
        lambda: print_store_items_amount(store),
        lambda: make_order(store),
        lambda: sys.exit()
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

        print()

def main():
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250)
    ]

    best_buy = Store(product_list)
    start(best_buy)


if __name__ == "__main__":
    main()
