from abc import ABC, abstractmethod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from products import Product


class Promotion(ABC):
    """
    Represents a base class for creating promotions assigned to product instances.
    """

    def __init__(self, name: str):
        """
        Initialize the promotion with the given name.

        :param name: The name of the promotion.
        :type name: str
        """
        Promotion._validate_name(name)
        self._name = name

    @staticmethod
    def _validate_name(name: str):
        """
        Validates the name of the promotion.

        :param name: The name to validate.
        :type name: str
        :raises ValueError: If the name is not a string or is empty.
        """
        if not isinstance(name, str):
            raise ValueError("Invalid promotion name set: name must be a string")
        if name == "":
            raise ValueError("Invalid promotion name set: name cannot be empty")

    @property
    def name(self) -> str:
        """
        Get the name of the promotion.

        :return: The name of the promotion.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """
        Set a new name for the promotion.

        :param name: The new promotion name.
        :type name: str
        """
        Promotion._validate_name(name)
        self._name = name

    @abstractmethod
    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """
        Apply the promotion to a product for a specific quantity.

        :param product: The product to apply the promotion on.
        :type product: Product
        :param quantity: The number of items.
        :type quantity: int
        :return: The final price after applying the promotion.
        :rtype: float
        """
        pass


class SecondHalfPrice(Promotion):
    """
    Promotion for products that applies a half-price discount for every other item.
    """

    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """
        Calculate the final price after applying a half-price discount for every other item.

        :param product: The product to apply the discount on.
        :type product: Product
        :param quantity: The number of items bought.
        :type quantity: int
        :return: The final price after the discount.
        :rtype: float
        """
        discount = (product.price / 2) * (quantity // 2)
        return (product.price * quantity) - discount


class ThirdOneFree(Promotion):
    """
    Promotion for products that applies a 100% discount for every third item.
    """

    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """
        Calculate the final price after applying a 100% discount for every third item.

        :param product: The product to apply the discount on.
        :type product: Product
        :param quantity: The number of items bought.
        :type quantity: int
        :return: The final price after the discount.
        :rtype: float
        """
        discount = product.price * (quantity // 3)
        return (product.price * quantity) - discount


class PercentDiscount(Promotion):
    """
    Promotion for products that applies a percentage discount to all items.
    The discount percentage is specified during instance creation.
    """

    def __init__(self, name: str, percent: int):
        """
        Initialize the PercentDiscount instance with a name and discount percentage.

        :param name: The name of the promotion.
        :type name: str
        :param percent: The percentage discount to apply (1-100% inclusive).
        :type percent: int
        :raises ValueError: If the percentage is out of the range 1-100.
        """
        super().__init__(name)
        if 0 > percent > 100:
            raise ValueError("Error creating percent discount: out of range 1 - 100 %")
        self.__percent = percent

    def apply_promotion(self, product: "Product", quantity: int) -> float:
        """
        Calculate the final price after applying a percentage discount to all items.

        :param product: The product to apply the discount on.
        :type product: Product
        :param quantity: The number of items bought.
        :type quantity: int
        :return: The final price after the discount.
        :rtype: float
        """
        discount = ((product.price / 100) * self.__percent)  # single product
        return (product.price - discount) * quantity
