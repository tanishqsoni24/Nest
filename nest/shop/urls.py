from django.urls import path, include
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shop/" , views.shop, name="shop"),
    path("product/<slug>/post-review/", views.post_review, name="post_review"),
    path("product/<slug>/", views.product, name="product"),
    path("cart/", views.view_cart, name="view_cart"),
    path("cart/clearcart/", views.clear_cart, name="clear_cart"),
    path("cart/<slug>/", views.cart, name="cart"),
    path("cart/removeitem/<slug>/", views.remove_item, name="remove_item"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
