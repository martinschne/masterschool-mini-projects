import pytest

from products import Product


def test_creating_normal_product():
    """
    Test the instantiation of the Product class with valid parameters.

    Verifies that:
    - The `name` attribute is set correctly.
    - The `price` attribute is set correctly.
    - The `_quantity` attribute is initialized as expected.
    - The `_active` attribute is True by default.
    """
    product = Product("Test name", 9.99, 100)
    assert product.name == "Test name"
    assert product.price == 9.99
    assert product._quantity == 100
    assert product._active == True


def test_creating_product_with_invalid_parameters():
    """
    Test the instantiation of the Product class with invalid parameters.

    Cases covered:
    - An empty name raises a ValueError.
    - A negative price raises a ValueError.
    - A negative quantity raises a ValueError.

    :raises ValueError: If any invalid parameter is passed to the constructor.
    """
    with pytest.raises(ValueError):
        Product("", -10, 100)
        Product("Test name", -10, 100)
        Product("Test name", 9.99, -100)


def test_product_inactive_on_quantity_zero():
    """
    Test that a product becomes inactive when its quantity is 0.

    Verifies that:
    - A product with an initial quantity of 0 is inactive.
    - Buying the last item of a product sets it to inactive.
    """
    product = Product("Test name", 9.99, 0)
    assert product._active == False

    product_quantity_one = Product("Test name", 9.99, 1)
    assert product_quantity_one.is_active() == True

    product_quantity_one.buy(1)

    # after buying last item the product should become inactive
    assert product_quantity_one.is_active() == False


def test_buy_product():
    """
    Test that buying a product updates its stock quantity and calculates the correct price.

    Verifies that:
    - The quantity decreases appropriately after a purchase.
    - The total price is calculated accurately.
    """
    product = Product("Test name", 9.99, 100)
    total_buying_price = product.buy(10)

    assert product.quantity == 90
    assert total_buying_price == 99.9


def test_buy_product_over_stock_quantity():
    """
    Test that attempting to buy more than the available stock raises an exception.

    :raises ValueError: If the quantity to buy exceeds the available stock.
    """
    product = Product("Test name", 9.99, 100)
    with pytest.raises(ValueError):
        product.buy(200)


pytest.main()
