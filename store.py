from products import Product


class Store:
    """
    Represents a store containing products in stock.
    """

    def __init__(self, products: list[Product]):
        """
        Initializes a Store instance with given products.
        @param products: (list[Product]) List of product to assign to the store.
        """
        self.products = products

    def add_product(self, product: Product):
        """
        Adds a product to the store.
        @param product: (Product) Product to be added to the store products.
        """
        self.products.append(product)

    def remove_product(self, product: Product):
        """
        Removes a product from the store.
        @param product: (Product) Product to be removed to the store products.
        """
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        """
        Get total quantity of all products in the store.
        @return: (int) Sum of quantities of all products in the store.
        """
        return sum(product._quantity for product in self.products)

    def get_all_products(self) -> list[Product]:
        """
        Returns all the active products in the store.
        @return: (list[Product]) Products with attribute 'active' set to True.
        """
        return [product for product in self.products if product._active]

    def order(self, shopping_list: list[tuple[Product, int]]) -> float:
        """
        Buy products from given shopping_list.
        @param shopping_list: (list[tuple[Product, int]]) List of order items.
        @return: (float) Total cost of the order.
        """
        total = 0
        for product, quantity in shopping_list:
            if product in self.products:
                total += product.buy(quantity)
                if not product.is_active():
                    self.remove_product(product)

        return total
