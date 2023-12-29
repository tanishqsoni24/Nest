from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User
from datetime import datetime
from shop.models import *
from django.utils import timezone

# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(unique=True, null=True, blank=True)
    forgot_password_otp = models.CharField(max_length=6, null=True, blank=True)
    is_account_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True, default=0, max_length=6)

    def get_cart_count(self):
        cart_obj = Cart.objects.filter(user = self.user, is_paid=False).first()
        cart_item = 0
        if cart_obj:
            for item in cart_obj.cart_items.all():
                cart_item += item.quantity
            return cart_item
            # return cart_obj.cart_items.count()
        return 0

    def __str__(self) -> str:
        return self.user.username + " - " + (lambda: "Not Verified", lambda: "Verified User")[self.is_account_verified]()
    
class Cart(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    is_paid = models.BooleanField(default=False)
    total = models.FloatField(default=0.0)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_signature = models.CharField(max_length=100, null=True, blank=True)
    payment_done_amount = models.IntegerField(default=0, null=True, blank=True)
    paid_cart_quantity = models.IntegerField(default=0, null=True, blank=True)
    publish_date = models.DateTimeField(default=timezone.now(),blank=True)

     # Delivery Details

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    phone2 = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=1000, null=True, blank=True)
    address2 = models.CharField(max_length=1000, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username + " - " + (lambda: "Not Paid", lambda: "Paid")[self.is_paid]()
    
class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)

    def __str__(self) -> str:
        return self.cart.user.username + " - " + self.product.p_name + " - " + str(self.quantity) + " - " + str(self.total)