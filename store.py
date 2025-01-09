class Store:
    def __init__(self, products: list):
       self.products = products

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        self.products.remove(product)

    def get_total_quantity(self) -> int:
        return sum(product.quantity for product in self.products)

    def get_all_products(self):
        return [product for product in self.products if product.active]

    def order(self, shopping_list) -> float:
        total = 0
        for product, quantity in shopping_list:
            if product in self.products:
                total += product.buy(quantity)

        return total