from django.contrib import admin
from shop.models import *

# Register your models here.

admin.site.register((Category, HomeCaraousel, Discount))

class ProductImageInline(admin.StackedInline):
    model = ProductImage

class ReviewsInline(admin.StackedInline):
    model = Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ReviewsInline]