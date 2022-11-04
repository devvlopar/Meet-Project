from django.urls import path
from . import views

urlpatterns = [
    path('', views.seller_index, name='seller_index'),
    path('add_products/', views.add_products, name="add_products"),
    path('seller_otp/', views.seller_otp, name="seller_otp"),
    path('login/', views.seller_login, name='seller_login'),
    path('logout/', views.seller_logout, name='seller_logout'),

    path('register/', views.seller_register, name='seller_register'),
    path('my_products/', views.my_products, name="my_products"),
    path('all_products/', views.ProductView.as_view())


]
