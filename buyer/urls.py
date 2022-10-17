from django.urls import path
from . import views
urlpatterns = [
    path("", views.index, name='index'),
    path('register/', views.register, name='register'),
    path('otp/', views.otp, name='otp'),
    path('shop/', views.shop, name='shop'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pk>', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<int:pk>', views.remove_item, name='remove_item'),
    path('cart/paymenthandler/', views.paymenthandler, name='paymenthandler'),




]
