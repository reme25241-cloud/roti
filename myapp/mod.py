
# models.py mainApplicationFunctionality20240625
# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    is_sold = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Wishlist(models.Model):
    added_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # added_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_proceeded = models.BooleanField(default=False)

    # @property
    # def total_price(self):
    #     cart_items = Cart.objects.filter(user=self.user, payment_proceeded=False)
    #     return sum(item.product.cost * item.quantity for item in cart_items)
    
    @property
    def total_price(self):
        cart_items = Cart.objects.filter(user=self.user, payment_proceeded=False)
        return sum(item.product.cost * item.quantity for item in cart_items)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.TextField()
    total_positive = models.PositiveIntegerField(default=0)
    total_negative = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class PendingPurchaseRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    payment_proceeded = models.BooleanField(default=False)
    seller_confirmed = models.BooleanField(default=False)
    buyer_received = models.BooleanField(default=False)

    # def mark_as_sold(self):
    #     if self.buyer_received:
    #         for item in Cart.objects.filter(user=self.user, payment_proceeded=True):
    #             item.product.is_sold = True
    #             item.product.save()
    
    def mark_as_sold(self):
        if self.buyer_received:
            cart_items = Cart.objects.filter(user=self.user, id=self.cart.id, payment_proceeded=True)
            for item in cart_items:
                item.product.is_sold = True
                item.product.save()
                

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"


class Return(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    reason_for_return = models.TextField()
    buyer_qr = models.ImageField(upload_to='qr/')
    is_returned = models.BooleanField(default=False)
    resell = models.BooleanField(default=False)

    def return_price(self):
        return round(self.product.cost * 0.8, 2)

    def process_return(self):
        if self.is_returned and self.resell:
            self.product.is_sold = False
            self.product.save()
