class Product:
    def __init__(self, name, price, quantity):
        if name == "":
            raise ValueError("Invalid name: name cannot be empty")
        if price < 0:
            raise ValueError(f"Invalid price: {price}, price can't be negative")
        if quantity < 0:
            raise ValueError(f"Invalid quantity: {quantity}, quantity can't be negative")

        self.name = name
        self.price = price
        self.quantity = quantity
        self.active = True

    def get_quantity(self) -> float:
        return self.quantity

    def set_quantity(self, quantity):
        self.quantity = quantity
        if self.quantity == 0:
            self.active = False

    def is_active(self) -> bool:
        return self.active

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def show(self) -> str:
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity) -> float:
        if quantity > self.quantity:
            raise ValueError("Requested quantity exceeds the stock")

        self.quantity -= quantity
        return quantity * self.price