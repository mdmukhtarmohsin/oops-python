# E-commerce Shopping Cart System

class Product:
    _products = []
    _category_sales = {}

    def __init__(self, product_id, name, price, category, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.stock_quantity = stock_quantity
        Product._products.append(self)

    def get_product_info(self):
        return {
            'id': self.product_id,
            'name': self.name,
            'price': self.price,
            'category': self.category,
            'stock_quantity': self.stock_quantity
        }

    @classmethod
    def get_total_products(cls):
        return len(cls._products)

    @classmethod
    def get_most_popular_category(cls):
        if not cls._category_sales:
            return None
        return max(cls._category_sales, key=cls._category_sales.get)

    def reduce_stock(self, quantity):
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            Product._category_sales[self.category] = Product._category_sales.get(self.category, 0) + quantity
            return True
        return False

class Customer:
    _customers = []
    _total_revenue = 0

    def __init__(self, customer_id, name, email, membership):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.membership = membership
        Customer._customers.append(self)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.membership}"

    def get_discount_rate(self):
        if self.membership == "premium":
            return 20
        elif self.membership == "gold":
            return 10
        return 0

    @classmethod
    def add_revenue(cls, amount):
        cls._total_revenue += amount

    @classmethod
    def get_total_revenue(cls):
        return cls._total_revenue

class ShoppingCart:
    def __init__(self, customer):
        self.customer = customer
        self.items = {} 

    def add_item(self, product, quantity):
        if product in self.items:
            self.items[product] += quantity
        else:
            self.items[product] = quantity

    def remove_item(self, product_id):
        for product in list(self.items.keys()):
            if product.product_id == product_id:
                del self.items[product]
                break

    def clear_cart(self):
        self.items.clear()

    def get_total_items(self):
        return sum(self.items.values())

    def get_cart_items(self):
        return {p.product_id: q for p, q in self.items.items()}

    def get_subtotal(self):
        return sum(product.price * quantity for product, quantity in self.items.items())

    def calculate_total(self):
        subtotal = self.get_subtotal()
        discount = self.customer.get_discount_rate()
        total = subtotal * (1 - discount / 100)
        return round(total, 2)

    def place_order(self):
        for product, quantity in self.items.items():
            if product.stock_quantity < quantity:
                return f"Insufficient stock for {product.name}"
        total = self.calculate_total()
        for product, quantity in self.items.items():
            product.reduce_stock(quantity)
        Customer.add_revenue(total)
        self.clear_cart()
        return "Order placed successfully"

laptop = Product("P001", "Gaming Laptop", 1299.99, "Electronics", 10)
book = Product("P002", "Python Programming", 49.99, "Books", 25)
shirt = Product("P003", "Cotton T-Shirt", 19.99, "Clothing", 50)

print(f"Product info: {laptop.get_product_info()}")
print(f"Total products in system: {Product.get_total_products()}")

customer = Customer("C001", "John Doe", "john@email.com", "premium")
cart = ShoppingCart(customer)

print(f"Customer: {customer}")
print(f"Customer discount: {customer.get_discount_rate()}%")

cart.add_item(laptop, 1)
cart.add_item(book, 2)
cart.add_item(shirt, 3)

print(f"Cart total items: {cart.get_total_items()}")
print(f"Cart subtotal: ${cart.get_subtotal()}")

final_total = cart.calculate_total()
print(f"Final total (with {customer.get_discount_rate()}% discount): ${final_total}")

print(f"Laptop stock before order: {laptop.stock_quantity}")
order_result = cart.place_order()
print(f"Order result: {order_result}")
print(f"Laptop stock after order: {laptop.stock_quantity}")

popular_category = Product.get_most_popular_category()
print(f"Most popular category: {popular_category}")

total_revenue = Customer.get_total_revenue()
print(f"Total revenue: ${total_revenue}")

cart.remove_item("P002")
print(f"Items after removal: {cart.get_cart_items()}")

cart.clear_cart()
print(f"Items after clearing: {cart.get_total_items()}")
