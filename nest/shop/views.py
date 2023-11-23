from django.shortcuts import render, redirect
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from accounts.models import Profile

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