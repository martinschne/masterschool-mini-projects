from promotions import Promotion


class Product:
    """
    Represents a product with a name, price, quantity in stock and promotion applied.
    """

    def __init__(self, name: str, price: float | int, quantity: int):
        """
        Initializes a Product instance with the given name, price, and quantity and no promotion.
        @param name: (str) The name of the product. Must not be empty.
        @param price: (float) The price of the product. Must be non-negative.
        @param quantity: (int) The quantity of the product in stock. Must be non-negative.
        @raise ValueError: If name is empty, price or quantity is negative.
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
        if not isinstance(name, str):
            raise ValueError("Invalid product name set: name must be a string")
        if name == "":
            raise ValueError("Invalid product name set: name cannot be empty")

    @staticmethod
    def _validate_price(price: float | int):
        if not isinstance(price, (float, int)):
            raise ValueError("Invalid price set: price must be a float")
        if price < 0:
            raise ValueError(f"Invalid price '{price}' set: price cannot be negative")

    @staticmethod
    def _validate_quantity(quantity: int):
        if not isinstance(quantity, int):
            raise ValueError("Invalid quantity set: quantity must be an int")
        if quantity < 0:
            raise ValueError(f"Invalid quantity '{quantity}' set: quantity cannot be negative")

    @property
    def name(self) -> str:
        """
        Returns the current name of the product.
        @return: (float) The name of the product.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        """
        Sets the name of the product.
        @param value: (float) The new name of the product.
        """
        Product._validate_name(value)
        self._name = value

    @property
    def price(self) -> float | int:
        """
        Returns the current price of the product in stock.
        @return: (float) The price of the product.
        """
        return self._price

    @price.setter
    def price(self, value: float | int):
        """
        Sets the price of the product in stock.
        @param value: (float) The new price of the product.
        """
        Product._validate_price(value)
        self._price = value

    @property
    def quantity(self) -> int:
        """
        Returns the current quantity of the product in stock.
        @return: (int) The quantity of the product.
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity: int):
        """
        Sets the quantity of the product in stock and updates its active status.
        @param quantity: (int) The new quantity of the product.
        """
        Product._validate_quantity(quantity)

        if quantity > 0:
            self.activate()
        else:
            self.deactivate()

        self._quantity = quantity

    @property
    def promotion(self) -> Promotion:
        """
        Returns the current promotion applied on the product.
        @return: (int) The promotion applied on the product.
        """
        return self._promotion

    @promotion.setter
    def promotion(self, promotion: Promotion):
        """
        Applies a new promotion on the product.
        @param promotion: (Promotion) The new promotion applied on the product.
        """
        if promotion is not None and not isinstance(promotion, Promotion):
            raise ValueError("Invalid promotion set: promotion must be an instance of Promotion or None")
        self._promotion = promotion

    def _get_promotion_name(self) -> str:
        """
        Returns the name of the promotion applied on the product as a string.
        If promotion was not applied on this product, it returns "None".
        @return: (str) promotion name or "None" if promotion was not set.
        """
        return getattr(self.promotion, 'name', "None")

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

    def __str__(self) -> str:
        """
        Allows printing a string representation of the product.
        @return: (str) Info containing the product's name, price, quantity and promotion applied.
        """
        return f"{self.name}, Price: ${self.price}, Quantity: {self.quantity}, Promotion: {self._get_promotion_name()}"

    def __eq__(self, other):
        """
        Enables comparison operator == between this product and other product instances.
        Compares prices of both products and returns the result as boolean.
        @param other: (Product) other product for price comparison.
        @return (bool) True if price of this product == price of other product, otherwise False.
        """
        return self.price == other.price

    def __ne__(self, other):
        """
        Enables comparison operator != between this product and other product instances.
        Compares prices of both products and returns the result as boolean.
        @param other: (Product) other product for price comparison.
        @return (bool) True if price of this product != price of other product, otherwise False.
        """
        return not self.__eq__(other)

    def __gt__(self, other: "Product"):
        """
        Enables comparison operator > between this product and other product instances.
        Compares prices of both products and returns the result as boolean.
        @param other: (Product) other product for price comparison.
        @return (bool) True if price of this product > price of other product, otherwise False.
        """
        return self.price > other.price

    def __ge__(self, other):
        """
        Enables comparison operator >= between this product and other product instances.
        Compares prices of both products and returns the result as boolean.
        @param other: (Product) other product for price comparison.
        @return (bool) True if price of this product >= price of other product, otherwise False.
        """
        return self.price >= other.price

    def __lt__(self, other):
        """
        Enables comparison operator < between this product and other product instances.
        Compares prices of both products and returns the result as boolean.
        @param other: (Product) other product for price comparison.
        @return (bool) True if price of this product < price of other product, otherwise False.
        """
        return self.price < other.price

    def __le__(self, other):
        """
        Enables comparison operator <= between this product and other product instances.
        Compares prices of both products and returns the result as boolean.
        @param other: (Product) other product for price comparison.
        @return (bool) True if price of this product <= price of other product, otherwise False.
        """
        return self.price <= other.price

    def buy(self, quantity: int) -> float:
        """
        Buys a specified quantity of the product.
        @param quantity: (int): The quantity to purchase.
        @return: (float) The total cost of the purchased quantity.
        @raise: ValueError: If the requested quantity exceeds the available stock.
        """
        product_quantity = self.quantity
        if quantity > product_quantity:
            raise ValueError("Error while making order! Quantity larger than what exists")

        self.quantity = product_quantity - quantity

        if self.promotion is not None:
            return self.promotion.apply_promotion(self, quantity)

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

    @Product.quantity.setter
    def quantity(self, quantity: int):
        """Custom setter for quantity in the child class."""
        print("Warning: Non-material product does not have a quantity.")

    def buy(self, quantity: int) -> float:
        """
        Returns total price of the non-stocked products ordered after applying the promotion.
        @return: (str) Info containing the product's name, price and quantity.
        Overrides standard Product method.
        """
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

    def __str__(self) -> str:
        """
        Allows printing a string representation of the limited product.
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
