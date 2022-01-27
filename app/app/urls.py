from django.contrib import admin
from django.urls import path, include, register_converter
from rest_framework.routers import DefaultRouter

from app import views

router = DefaultRouter()
router.register("products", views.ProductApiView)
router.register("category", views.CategoryApiView)
# router.register("products_info", views.ProductInfoApiView)


urlpatterns = [
    path('', include(router.urls)),
    path('', views.home_view, name='home'),
    path('users/', views.users_view, name='users'),
    # path('products/', views.products_view, name='products'),
    path('products/<slug:slug>/', views.products_detail_view, name='products_detail'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
]
