from django.db import models
from base.models import BaseModel

# Create your models here.

class Product(BaseModel):
    p_name = models.CharField(max_length=255)
    p_slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)
    p_description = models.TextField()
    p_mrp = models.FloatField(blank=True, null=True)
    p_price = models.FloatField(blank=True, null=True)
    p_image = models.ImageField(upload_to="product_images")
    p_category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products")
    p_buy_count = models.IntegerField(default=0)
    p_discount = models.ForeignKey("Discount", on_delete=models.SET_NULL, related_name="products", blank=True, null=True)

    def __str__(self) -> str:
        return self.p_name
    
    def save(self, *args, **kwargs):
        self.p_slug = self.p_name.replace(" ", "-").lower()
        self.p_price = self.p_mrp - (self.p_mrp * (self.p_discount.d_percentage / 100))
        super().save(*args, **kwargs)  

class ProductImage(BaseModel):
    pi_image = models.ImageField(upload_to="product_images")
    pi_product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="images")

    def __str__(self) -> str:
        return self.pi_product.p_name + " - " + str(self.pi_image) 
    
class Category(BaseModel):
    c_name = models.CharField(max_length=255)
    c_image = models.ImageField(upload_to="category_images", blank=True, null=True)
    # c_buy_count = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.c_name
    
class HomeCaraousel(BaseModel):
    hc_title = models.CharField(max_length=255)
    hc_description = models.TextField()
    hc_image = models.ImageField(upload_to="home_carousel_images")

    def __str__(self) -> str:
        return self.hc_title

class Discount(BaseModel):
    d_percentage = models.FloatField()

    def __str__(self) -> str:
        return str(self.d_percentage) + "%"
    
class Review(BaseModel):
    r_review = models.TextField()
    r_product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="reviews")
    r_user = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.r_product.p_name + " - " + self.r_user.user.username + " - " + self.r_review[:10] + "..."