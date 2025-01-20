class Product:
    """
    Represents a product with a name, price, and quantity in stock.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a Product instance with the given name, price, and quantity.
        :param name: (str) The name of the product. Must not be empty.
        :param price: (float) The price of the product. Must be non-negative.
        :param quantity: (int) The quantity of the product in stock. Must be non-negative.
        :raises ValueError: If name is empty, price is negative, or quantity is negative.
        """
        if name == "":
            raise ValueError("Invalid name: name cannot be empty")
        if price < 0:
            raise ValueError(f"Invalid price: {price}, price can't be negative")
        if quantity < 0:
            raise ValueError(f"Invalid quantity: {quantity}, quantity can't be negative")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = quantity > 0

    def get_quantity(self) -> int:
        """
        Returns the current quantity of the product in stock.
        :returns: (int) The quantity of the product.
        """
        return self.quantity

    def set_quantity(self, quantity: int):
        """
        Set the quantity of the product in stock and updates its active status.
        :param quantity: (int) The new quantity of the product.
        """
        if quantity > 0:
            self.activate()
        else:
            self.deactivate()

        self.quantity = quantity

    def is_active(self) -> bool:
        """
        Checks if the product is active.
        :returns: (bool) True if the product is active, False otherwise.
        """
        return self.active

    def activate(self):
        """Activates the product, setting its status to active."""
        self.active = True

    def deactivate(self):
        """Deactivates the product, setting its status to inactive."""
        self.active = False

    def show(self) -> str:
        """
        Returns a string representation of the product.
        :returns A string containing the product's name, price, and quantity.
        """
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity: int) -> float:
        """
        Buys a specified quantity of the product.
        :param quantity: (int): The quantity to purchase.
        :returns: (float) The total cost of the purchased quantity.
        :raises: ValueError: If the requested quantity exceeds the available stock.
        """
        product_quantity = self.get_quantity()
        if quantity > product_quantity:
            raise ValueError("Requested quantity exceeds the stock")

        self.set_quantity(product_quantity - quantity)

        return quantity * self.price
