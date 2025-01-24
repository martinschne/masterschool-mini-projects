from promotions import Promotion


class Product:
    """
    Represents a product with a name, price, quantity in stock and promotion applied.
    """

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initializes a Product instance with the given name, price, and quantity and no promotion.
        @param name: (str) The name of the product. Must not be empty.
        @param price: (float) The price of the product. Must be non-negative.
        @param quantity: (int) The quantity of the product in stock. Must be non-negative.
        @raise ValueError: If name is empty, price is negative, or quantity is negative.
        """
        if name == "":
            raise ValueError("Invalid name: name cannot be empty")
        if price < 0:
            raise ValueError(f"Invalid price: {price}, price can't be negative")
        if quantity < 0:
            raise ValueError(f"Invalid quantity: {quantity}, quantity can't be negative")

        self.name = name
        self.price = price
        self._quantity = quantity
        self._active = quantity > 0
        self._promotion = None

    def get_quantity(self) -> int:
        """
        Returns the current quantity of the product in stock.
        @return: (int) The quantity of the product.
        """
        return self._quantity

    def set_quantity(self, quantity: int):
        """
        Set the quantity of the product in stock and updates its active status.
        @param quantity: (int) The new quantity of the product.
        """
        if quantity > 0:
            self.activate()
        else:
            self.deactivate()

        self._quantity = quantity

    def get_promotion(self) -> Promotion:
        """
        Returns the current promotion applied on the product.
        @return: (int) The promotion applied on the product.
        """
        return self._promotion

    def set_promotion(self, promotion: Promotion):
        """
        Applies a new promotion on the product.
        @param promotion: (Promotion) The new promotion applied on the product.
        """
        if promotion is not None and not isinstance(promotion, Promotion):
            raise ValueError("promotion must be an instance of Promotion or None")
        self._promotion = promotion

    def _get_promotion_name(self) -> str:
        """
        Returns the name of the promotion applied on the product as a string.
        If promotion was not applied on this product, it returns "None".
        @return: (str) promotion name or "None" if promotion was not set.
        """
        return getattr(self.get_promotion(), 'get_name', lambda: "None")()

    def is_active(self) -> bool:
        """
        Checks if the product is active.
        @return: (bool) True if the product is active, False otherwise.
        """
        return self._active

    def activate(self):
        """Activates the product, setting its status to active."""
        self._active = True

    def deactivate(self):
        """Deactivates the product, setting its status to inactive."""
        self._active = False

    def show(self) -> str:
        """
        Returns a string representation of the product.
        @return: (str) Info containing the product's name, price, quantity and promotion applied.
        """
        return f"{self.name}, Price: ${self.price}, Quantity: {self._quantity}, Promotion: {self._get_promotion_name()}"

    def buy(self, quantity: int) -> float:
        """
        Buys a specified quantity of the product.
        @param quantity: (int): The quantity to purchase.
        @return: (float) The total cost of the purchased quantity.
        @raise: ValueError: If the requested quantity exceeds the available stock.
        """
        product_quantity = self.get_quantity()
        if quantity > product_quantity:
            raise ValueError("Error while making order! Quantity larger than what exists")

        self.set_quantity(product_quantity - quantity)

        promotion = self.get_promotion()
        if promotion is not None:
            return promotion.apply_promotion(self, quantity)

        return quantity * self.price


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        """
        Initializes a NonStockedProduct instance with the given name and price.
        @param name: (str) The name of the product. Must not be empty.
        @param price: (float) The price of the product. Must be non-negative.
        @raise ValueError: If name is empty, price is negative, or quantity is negative.
        Quantity of the product stays allways 0 and the product is activated on creation.
        """
        super().__init__(name, price, 0)
        super().activate()

    def set_quantity(self, quantity: int):
        """ Prints warning when user calls this method on non-material product. """
        print("Warning: non stocked product does not have a quantity.")

    def show(self) -> str:
        """
        Returns a string representation of the non-stocked product.
        @return: (str) Info containing the product's name, price, quantity and promotion applied.
        Overrides standard Product method.
        """
        return f"{self.name}, Price: ${self.price}, Quantity: Unlimited, Promotion: {self._get_promotion_name()}"

    def buy(self, quantity: int) -> float:
        """
        Returns total price of the non-stocked products ordered after applying the promotion.
        @return: (str) Info containing the product's name, price and quantity.
        Overrides standard Product method.
        """
        promotion = self.get_promotion()
        if promotion is not None:
            return promotion.apply_promotion(self, quantity)

        return quantity * self.price


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """
        Initializes a LimitedProduct instance with the given name, price, quantity and maximum.
        @param name: (str) The name of the product. Must not be empty.
        @param price: (float) The price of the product. Must be non-negative.
        @param quantity: (int) The quantity of the product in stock. Must be non-negative.
        @param maximum: (int) Maximum quantity allowed in one order for this product.
        @raise ValueError: If name is empty, price is negative, or quantity is negative.
        """
        super().__init__(name, price, quantity)
        self._maximum = maximum

    def show(self) -> str:
        """
        Returns a string representation of the limited product.
        @return: (str) Info containing the product's name, price, quantity and promotion applied.
        Overrides standard Product method.
        """
        return f"{self.name}, Price: ${self.price}, Limited to 1 per order!, Promotion: {self._get_promotion_name()}"

    def buy(self, quantity: int) -> float:
        if quantity > self._maximum:
            raise ValueError(
                f"Error while making order! Only {self._maximum} is allowed from this product1!"
            )
        return super().buy(quantity)
