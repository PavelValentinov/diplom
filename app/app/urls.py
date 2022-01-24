from django.urls import path

from app import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('users/', views.users_view, name='users'),
    path('products/', views.products_view, name='products'),
    path('register/', views.register, name='register'),
]
