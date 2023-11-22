from django.db import models
from base.models import BaseModel
from django.contrib.auth.models import User

# Create your models here.

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    email = models.EmailField(unique=True, null=True, blank=True)
    forgot_password_otp = models.CharField(max_length=6, null=True, blank=True)
    is_account_verified = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True, default=0, max_length=6)

    # def get_cart_count(self):
    #     Cart_Items =  CartItems.objects.filter(cart__is_paid = False, cart__user=self.user)
    #     cart_total = sum([cart_item.quantity if cart_item.product.product_available_count > 0 else 0 for cart_item in Cart_Items])
    #     return cart_total

    def __str__(self) -> str:
        return self.user.username + " - " + (lambda: "Not Verified", lambda: "Verified User")[self.is_account_verified]()
    
