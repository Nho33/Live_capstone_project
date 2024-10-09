from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#model for product category

class Category(models.Model):
    name = models.CharField(max_length = 80)
    
    def __str__(self):
        return self.name

# model for products

class Product(models.Model):
    name = models.CharField(max_length = 80)
    description = models.TextField(blank=True) # description field is optional on the order form
    order_date = models.DateTimeField(auto_now_add=True) #time stamp for discounts and promotions
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    stock = models.IntegerField()#Howw many of these products do we have in stock
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) #There's a many to one relationship between product and category. One category can have many products. When the category liked to the product is deleted, then the category field in the form will be null.  


    def __str__(self):
        return self.name

# model for Customer or user purchasing

class Customer(models.Model):
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 10)
    user = models.OneToOneField(User, on_delete = models.CASCADE) #When the user is delted, then the entire profile associated with the user is also deleted

    def __str__(self):
        return self.user.username
#model for tracking customer orders
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, null = True)
    order_date = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False)
    transaction_id = models.CharField(max_length = 100, null = True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.user.username}"

#model for the products in an order

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order, on_delete = models.CASCADE, related_name = "order_items")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
#model for tracking the current items on the user's cart

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return f"Here's your cart {self.customer.user.username}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in the cart"
    
    # ShippingAddress model to store shipping information for an order
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"The order will be delivered to this address for {self.customer.user.username}"

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=100)  # E.g., Credit Card, PayPal
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.order.id} - {self.amount}"




