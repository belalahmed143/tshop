from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home' ),
    path('product_category_list/',product_category_list, name='category-list'),
    path('product_category/<name>/', product_category, name='product-category'),

    # path('product_details/<slug>/',ProductDetailsView.as_view(), name='product-detail'),
    path('product_details/<slug>/',product_details, name='product-detail'),

    
    path('add_to_cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('cart_summary', CartSummaryView.as_view(), name='cart-summary'),
    path('cart_product_increment/<slug>/', cart_product_increment, name='cart-product-increment'),
    path('cart_product_decrement/<slug>/', cart_product_decrement, name='cart-product-decrement'),
    path('cart_delete/<slug>/', cart_delete, name='cart-delete'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('customerorderstatus/', CustomerOrderStatusView.as_view(), name='customer-order-status'),

    path('search/', ProductSearch, name='search'),
]
 