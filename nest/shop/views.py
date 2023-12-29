from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from accounts.models import *

# Create your views here.

@csrf_exempt
def index(request):
    categories = Category.objects.all()
    carousel_data = HomeCaraousel.objects.all()
    ten_popular_produts = Product.objects.all().order_by("-p_buy_count")[:10]
    context = {
        "categories" : categories,
        "carousel_data" : carousel_data,
        "ten_popular_produts" : ten_popular_produts
    }
    return render(request, "shop/index.html", context)

@csrf_exempt
def shop(request):
    all_products = Product.objects.all()
    categories = Category.objects.all()
    context = {
        "products" : all_products,
        "categories" : categories
    }
    # return HttpResponse(context["products"])
    return render(request, "shop/shop.html", context)

@csrf_exempt
def product(request, slug):
    product = Product.objects.filter(p_slug = slug).first()
    related_products = Product.objects.filter(p_category = product.p_category).exclude(p_slug = slug)
    context = {
        "product" : product,
        "related_products" : related_products
    }
    return render(request, "shop/product-description.html", context)

def post_review(request, slug):
    if request.method == "POST":
        product = Product.objects.filter(p_slug = slug).first()
        user = request.user
        profle_obj = Profile.objects.filter(user = user).first()
        review = request.POST.get("review")
        print(review, product, profle_obj, user)
        review_obj = Review.objects.create(r_review = review, r_product = product, r_user = profle_obj)
        review_obj.save()
        return redirect("/product/" + slug + "/")
    return HttpResponse("Invalid Request")

def cart(request, slug):
    if request.user.is_authenticated:
        product = Product.objects.filter(p_slug = slug).first()
        user = request.user
        cart_obj = Cart.objects.filter(user = user, is_paid=False).first()
        if not cart_obj:
            cart_obj = Cart.objects.create(user = user)
            cart_obj.save()
            cart_item_obj = CartItems.objects.filter(cart = cart_obj, product = product).first()
            if cart_item_obj:
                cart_item_obj.quantity += 1
                cart_item_obj.total += product.p_price
                cart_item_obj.save()
            else:
                cart_item_obj = CartItems.objects.create(cart = cart_obj, product = product, quantity = 1, price = product.p_price, total = product.p_price)
                cart_item_obj.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        cart_item_obj = CartItems.objects.filter(cart = cart_obj, product = product).first()
        if cart_item_obj:
            cart_item_obj.quantity += 1
            cart_item_obj.total += product.p_price
            cart_item_obj.save()
        else:
            cart_item_obj = CartItems.objects.create(cart = cart_obj, product = product, quantity = 1, price = product.p_price, total = product.p_price)
            cart_item_obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponse("Invalid Request")

def view_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_obj = Cart.objects.filter(user = user, is_paid=False).first()
        if not cart_obj:
            return HttpResponse("Cart is Empty")
        cart_items = cart_obj.cart_items.all()
        context = {
            "cart_items" : cart_items,
            "cart" : cart_obj
        }
        return render(request, "shop/cart.html", context)
    return HttpResponse("Invalid Request")

def clear_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_obj = Cart.objects.filter(user = user, is_paid=False).first()
        if not cart_obj:
            return HttpResponse("Cart is Empty")
        cart_items = cart_obj.cart_items.all()
        cart_items.delete()
        return redirect("/cart/")
    return HttpResponse("Invalid Request")

def remove_item(request, slug):
    if request.user.is_authenticated:
        user = request.user
        cart_obj = Cart.objects.filter(user = user, is_paid=False).first()
        if not cart_obj:
            return HttpResponse("Cart is Empty")
        product = Product.objects.filter(p_slug = slug).first()
        cart_item_obj = CartItems.objects.filter(cart = cart_obj, product = product).first()
        if not cart_item_obj:
            return HttpResponse("Item Not Found")
        cart_item_obj.delete()
        return redirect("/cart/")
    return HttpResponse("Invalid Request")

def about(request):
    return render(request, "shop/about.html")

def contact(request):
    return render(request, "shop/contact.html")