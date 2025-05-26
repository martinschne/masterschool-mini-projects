# Bestbuy 2

An enhanced version of the bestbuy project, this simple terminal application utilizes advanced OOP techniques built with Python.

It provides the same basic operations as **bestbuy**:

- Adding and removing products
- Querying the total quantity of stock
- Ordering products

Additionally, it offers more features:

- **Combining Stores**: Merge multiple stores for easier inventory management.  
  - *Technical Detail*: Uses the overloaded `__add__` operator to combine store objects.


- **Product Comparison**: Easily compare products to find the best option.  
  - *Technical Detail*: Implemented with overloaded comparison operators for intuitive comparisons.


- **Stock Distinction**: Identify non-stocked and limited products.  
  - *Technical Detail*: Utilizes inheritance to create specific product classes.


- **Special Promotions**: Apply promotions that affect product pricing.  
  - *Technical Detail*: Calculates the final order price by applying relevant discounts.

 
## Usage:

1. **Run the app**:
   ```bash
   python main.py