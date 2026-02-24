from django.urls import path
from . import views

urlpatterns = [
    path('',          views.login_page,    name='login_page'),
    path('login/',    views.login_view,    name='login'),
    path('register/', views.register_view, name='register'),
    path('guest/',    views.guest_view,    name='guest'),
    path('logout/',   views.logout_view,   name='logout'),
    path('products/', views.products_view, name='products'),
]