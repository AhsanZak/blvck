from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user-login/', views.user_login, name='user_login'),
    path('otp-login/', views.otp_login, name="otp_login"),
    path('otp', views.verify_otp, name="verify_otp"),

    path('user-signup/', views.user_signup, name='user_signup'),
    path('view-single/<int:id>', views.view_single, name="single"),
    path('user-home/', views.user_home, name="user_home"),
    path('user-profile/', views.user_profile, name="user_profile"),
    path('user-editprofile/', views.edit_user_profile, name="edit_userProfile"),
    path('user_logout', views.user_logout, name="user_logout"),

    path('add-cart/<int:id>', views.add_cart, name="add_cart"),
    path('cart/', views.cart, name="cart"),
    path('cart/update/<int:id>', views.cart_update, name="cart_update"),

    path('add-address', views.add_address, name="add_address"),

    path('checkout/', views.checkout, name="checkout"),

    path('user-payment/<int:id>', views.user_payment, name="user_payment"),
    path('user-order/', views.user_order, name="user_order"),
    path('user-removeOrderItem/<int:id>', views.user_remove_order_item, name="user_removeOrderItem"),
    path('success-paypal/', views.success_paypal, name="success_paypal"),
    path('success-razorpay/', views.success_razorpay, name="success_razorpay"),

    path('razorpay', views.razorpay, name="razorpay"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
