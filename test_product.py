import pytest

from products import Product


def test_creating_normal_product():
    """ Tests instantiation of the Product class with valid parameters. """
    product = Product("Test name", 9.99, 100)
    assert product.name == "Test name"
    assert product.price == 9.99
    assert product.quantity == 100
    assert product.active == True


def test_creating_product_with_invalid_parameters():
    """
    Tests instantiation of Product class with invalid parameters:
    - empty name
    - negative price
    - negative quantity
    """
    with pytest.raises(ValueError):
        Product("", -10, 100)
        Product("Test name", -10, 100)
        Product("Test name", 9.99, -100)


def test_product_inactive_on_quantity_zero():
    """
    Tests that newly created product with quantity set to 0 is inactive.
    Also test that buying last item makes the product inactive.
    """
    product = Product("Test name", 9.99, 0)
    assert product.active == False

    product_quantity_one = Product("Test name", 9.99, 1)
    assert product_quantity_one.is_active() == True

    product_quantity_one.buy(1)

    # after buying last item the product should become inactive
    assert product_quantity_one.is_active() == False


def test_buy_product():
    """
    Tests that buying product changes its stock quantity.
    Verify that buying operation returns correct total price.
    """
    product = Product("Test name", 9.99, 100)
    total_buying_price = product.buy(10)

    assert product.get_quantity() == 90
    assert total_buying_price == 99.9


def test_buy_product_over_stock_quantity():
    """ Tests that buying more than available quantity raises an exception. """
    product = Product("Test name", 9.99, 100)
    with pytest.raises(ValueError):
        product.buy(200)


pytest.main()
