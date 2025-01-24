from promotions import Promotion


class Product:
    """
    Represents a product with a name, price, quantity in stock, and promotion applied.
    """

    def __init__(self, name: str, price: float | int, quantity: int):
        """
        Initializes a Product instance with the given name, price, and quantity, and no promotion.
        @param name: (str) The name of the product. Must not be empty.
        @param price: (float | int) The price of the product. Must be non-negative.
        @param quantity: (int) The quantity of the product in stock. Must be non-negative.
        @raise ValueError: If name is empty, price is negative, or quantity is negative.
        """
        Product._validate_name(name)
        self._name = name

        Product._validate_price(price)
        self._price = price

        Product._validate_quantity(quantity)
        self._quantity = quantity

        self._active = quantity > 0
        self._promotion = None

    @staticmethod
    def _validate_name(name: str):
        """
        Validates the product name.
        @param name: (str) The name to validate.
        @raise ValueError: If the name is not a string or is empty.
        """
        if not isinstance(name, str):
            raise ValueError("Invalid product name set: name must be a string")
        if name == "":
            raise ValueError("Invalid product name set: name cannot be empty")

    @staticmethod
    def _validate_price(price: float | int):
        """
        Validates the product price.
        @param price: (float | int) The price to validate.
        @raise ValueError: If the price is not a number or is negative.
        """
        if not isinstance(price, (float, int)):
            raise ValueError("Invalid price set: price must be a float")
        if price < 0:
            raise ValueError(f"Invalid price '{price}' set: price cannot be negative")

    @staticmethod
    def _validate_quantity(quantity: int):
        """
        Validates the product quantity.
        @param quantity: (int) The quantity to validate.
        @raise ValueError: If the quantity is not an integer or is negative.
        """
        if not isinstance(quantity, int):
            raise ValueError("Invalid quantity set: quantity must be an int")
        if quantity < 0:
            raise ValueError(f"Invalid quantity '{quantity}' set: quantity cannot be negative")

    @property
    def name(self) -> str:
        """Returns the name of the product."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Sets the name of the product."""
        Product._validate_name(value)
        self._name = value

    @property
    def price(self) -> float | int:
        """Returns the price of the product."""
        return self._price

    @price.setter
    def price(self, value: float | int):
        """Sets the price of the product."""
        Product._validate_price(value)
        self._price = value

    @property
    def quantity(self) -> int:
        """"Returns the quantity of the product in stock."""
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """Sets the quantity of the product and updates its active status."""
        Product._validate_quantity(quantity)

        if quantity > 0:
            self.activate()
        else:
            self.deactivate()

        self._quantity = quantity

    @property
    def promotion(self) -> Promotion:
        """Returns the current promotion applied to the product."""
        return self._promotion

    @promotion.setter
    def promotion(self, promotion: Promotion):
        """
        Sets the promotion for the product.
        @param promotion: (Promotion) A promotion object or None.
        @raise ValueError: If promotion is not an instance of Promotion or None.
        """
        if promotion is not None and not isinstance(promotion, Promotion):
            raise ValueError("Invalid promotion set: promotion must be an instance of Promotion or None")
        self._promotion = promotion

    def _get_promotion_name(self) -> str:
        """Returns the name of the promotion applied to the product, or 'None' if no promotion is set."""
        return getattr(self.promotion, 'name', "None")

    def is_active(self) -> bool:
        """Returns whether the product is active."""
        return self._active

    def activate(self):
        """Activates the product."""
        self._active = True

    def deactivate(self):
        """Deactivates the product."""
        self._active = False

    def __str__(self) -> str:
        """
        Returns a string representation of the product.
        Includes the name, price, quantity, and applied promotion.
        """
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Promotion: {self._get_promotion_name()}"

    def __eq__(self, other):
        """Checks equality of prices between two products."""
        return self.price == other.price

    def __ne__(self, other):
        """Checks inequality of prices between two products."""
        return not self.__eq__(other)

    def __gt__(self, other: "Product"):
        """Compares whether this product is more expensive than another."""
        return self.price > other.price

    def __ge__(self, other):
        """Compares whether this product is more expensive than another or equally priced."""
        return self.price >= other.price

    def __lt__(self, other):
        """Compares whether this product is less expensive than another."""
        return self.price < other.price

    def __le__(self, other):
        """Compares whether this product is less expensive or equally priced."""
        return self.price <= other.price

    def buy(self, quantity: int) -> float:
        """
        Buys a specified quantity of the product.
        @param quantity: (int) The quantity to purchase.
        @return: (float) The total cost of the purchased quantity.
        @raise ValueError: If the requested quantity exceeds available stock.
        """
        product_quantity = self.quantity
        if quantity > product_quantity:
            raise ValueError("Error while making order! Quantity larger than what exists")

        self.quantity = product_quantity - quantity

        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)

        return quantity * self.price


class NonStockedProduct(Product):
    """
    Represents a non-stocked product with unlimited availability.
    """

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

    @Product.quantity.setter
    def quantity(self, quantity: int):
        """Prevents setting a quantity for non-stocked products."""
        print("Warning: Non-material product does not have a quantity.")

    def buy(self, quantity: int) -> float:
        """Returns the total price of non-stocked products ordered."""
        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)

        return quantity * self.price

    def __str__(self) -> str:
        """
        Allows printing a string representation of the non-stocked product.
        @return: (str) Info containing the product's name, price, quantity () and promotion applied.
        """
        return f"{self.name}, Price: ${self.price}, Quantity: Unlimited, Promotion: {self._get_promotion_name()}"


class LimitedProduct(Product):
    """
    Represents a product with a maximum purchase limit per order.
    """

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self._maximum = maximum

    def __str__(self) -> str:
        """
        Allows printing a string representation of the limited product.
        @return: (str) Info containing the product's name, price, quantity and promotion applied.
        Overrides standard Product method.
        """
        return f"{self.name}, Price: ${self.price}, Limited to 1 per order!, Promotion: {self._get_promotion_name()}"

    def buy(self, quantity: int) -> float:
        """
        Buys a specified quantity of the limited product.
        @param quantity: (int) The quantity to purchase.
        @raise ValueError: If the quantity exceeds the maximum allowed per order.
        """
        if quantity > self._maximum:
            raise ValueError(
                f"Error while making order! Only {self._maximum} is allowed from this product1!"
            )
        return super().buy(quantity)
