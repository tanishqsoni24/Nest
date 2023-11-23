from django.urls import path, include
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("shop/" , views.shop, name="shop"),
    path("product/<slug>/post-review/", views.post_review, name="post_review"),
    path("product/<slug>/", views.product, name="product"),
]
