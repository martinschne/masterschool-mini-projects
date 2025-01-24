from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    Represents a base for creating promotions assigned to product instances.
    """

    def __init__(self, name: str):
        """
        Instantiates the promotion with given name.
        @param name: (str) name of the promotion.
        """
        Promotion._validate_name(name)
        self._name = name

    @staticmethod
    def _validate_name(name: str):
        if not isinstance(name, str):
            raise ValueError("Invalid promotion name set: name must be a string")
        if name == "":
            raise ValueError("Invalid promotion name set: name cannot be empty")

    @property
    def name(self) -> str:
        """
        Returns the name of the promotion.
        @return: (str) name of the promotion.
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Applies a new promotion on the product.
        @param name: (str) The new promotion applied on the product.
        """
        Promotion._validate_name(name)
        self._name = name

    @abstractmethod
    def apply_promotion(self, product: "Product", quantity: int) -> float:
        pass


class SecondHalfPrice(Promotion):
    """
    Promotion for products applying half price discount for every other item.
    """

    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """
        Returns final price after applying half price discount for every other item.
        @param product: (Product) product to apply the discount on.
        @param quantity: (int) number of items bought.
        @return: (float) final price after discount.
        Provides specific implementation of abstract promotion method.
        """
        discount = (product.price / 2) * (quantity // 2)  # even items at half
        return (product.price * quantity) - discount


class ThirdOneFree(Promotion):
    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """
        Returns final price after applying 100% discount for every third item.
        @param product: (Product) product to apply the discount on.
        @param quantity: (int) number of items bought.
        @return: (float) final price after discount.
        Provides specific implementation of abstract promotion method.
        """
        discount = product.price * (quantity // 3)  # all third items
        return (product.price * quantity) - discount


class PercentDiscount(Promotion):
    """
    Represents promotion for products applying percentual discount on all items.
    Percentage is specified at instance creation as a private instance variable.
    """

    def __init__(self, name: str, percent: int):
        """
        Initiate the PercentDiscount instance with given parameters.
        @param name: (str) name of the promotion.
        @param percent: (int) percentage discounted from price in range 1 - 100 % inclusive.
        """
        super().__init__(name)
        if 0 > percent > 100:
            raise ValueError("Error creating percent discount: out of range 1 - 100 %")
        self.__percent = percent

    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """
        Returns final price after applying percentual discount on all items.
        @param product: (Product) product to apply the discount on.
        @param quantity: (int) number of items bought.
        @return: (float) final price after discount.
        Provides specific implementation of abstract promotion method.
        """
        discount = ((product.price / 100) * self.__percent)  # single product
        return (product.price - discount) * quantity
