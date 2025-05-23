from products import Product


class Store:
    """
    Represents a store containing products in stock.
    """

    def __init__(self, products: list[Product]):
        """
        Initializes a Store instance with the given products.

        :param products: List of products to assign to the store.
        :type products: list[Product]
        """
        self.products = products

    def add_product(self, product: Product):
        """
        Adds a product to the store.

        :param product: Product to be added to the store.
        :type product: Product
        """
        self.products.append(product)

    def remove_product(self, product: Product):
        """
        Removes a product from the store.

        :param product: Product to be removed from the store.
        :type product: Product
        """
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """
        Gets the total quantity of all products in the store.

        :return: Sum of the quantities of all products in the store.
        :rtype: int
        """
        return sum(product.quantity for product in self.products)

    def get_all_products(self) -> list[Product]:
        """
        Returns all active products in the store.

        :return: A list of products with the attribute ``active`` set to True.
        :rtype: list[Product]
        """
        return [product for product in self.products if product.is_active()]

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        """
        Processes an order by purchasing products from the given shopping list.

        :param shopping_list: List of order items, where each item is a tuple
                              containing a product and the quantity to purchase.
        :type shopping_list: list[tuple[Product, int]]
        :return: Total cost of the order.
        :rtype: float
        :raises ValueError: If the requested quantity exceeds available stock for any product.
        """
        total = 0
        for product, quantity in shopping_list:
            if product in self.products:
                total += product.buy(quantity)
                if not product.is_active():
                    self.remove_product(product)

        return total

    def __contains__(self, item: Product):
        """
        Checks if the given product is in the store's active product list.

        :param item: Product to check for in the store.
        :type item: Product
        :return: True if the product is in the store, otherwise False.
        :rtype: bool
        """
        return item in self.get_all_products()

    def __add__(self, other_store: "Store"):
        """
        Combines the products of this store with those of another store, creating a new store.

        :param other_store: Another store to combine with this store.
        :type other_store: Store
        :return: A new store containing products from both stores.
        :rtype: Store
        :raises NotImplementedError: If the other_store is not an instance of the Store class.
        """
        if isinstance(other_store, Store):
            return Store(self.products + other_store.products)
        return NotImplemented
